from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import (
    CodeTaskAlreadyUsedError,
    CodeTaskNotFoundError,
    SectionNotFoundError,
)
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User


@dataclass(slots=True)
class DeleteCodeTaskCommand:
    actor: User
    code_task_id: UUID


class DeleteCodeTaskUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteCodeTaskCommand) -> None:
        async with self.uow:
            code_task = await self.uow.code_tasks.get_by_id(
                command.code_task_id
            )
            if code_task is None:
                raise CodeTaskNotFoundError('Code task not found.')

            await self.course_access_service.ensure_can_manage_section(
                actor=command.actor,
                section_id=code_task.section_id,
            )

            has_attempts = await (
                self.uow.code_submissions.exists_by_code_task_id(code_task.id)
            )
            if has_attempts:
                raise CodeTaskAlreadyUsedError(
                    'Code task already has student submissions '
                    'and cannot be changed safely.'
                )

            section = await self.uow.sections.get_by_id(code_task.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')

            test_cases = await self.uow.test_cases.get_by_ids(
                code_task.test_case_ids
            )
            for test in test_cases:
                await self.uow.test_cases.remove(test)

            section.remove_code_task(code_task.id)
            await self.uow.sections.update(section)
            await self.uow.code_tasks.remove(code_task)
            await self.uow.commit()
