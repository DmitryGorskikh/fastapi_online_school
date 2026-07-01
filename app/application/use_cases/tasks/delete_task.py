from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import (
    TaskAlreadyUsedError,
    TaskNotFoundError,
    SectionNotFoundError,
)
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User


@dataclass(slots=True)
class DeleteTaskCommand:
    actor: User
    task_id: UUID


class DeleteTaskUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteTaskCommand) -> None:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(command.task_id)
            if task is None:
                raise TaskNotFoundError('Task not found.')

            await self.course_access_service.ensure_can_manage_section(
                actor=command.actor,
                section_id=task.section_id,
            )

            has_attempts = await (
                self.uow.task_attempts.exists_by_task_id(task.id)
            )
            if has_attempts:
                raise TaskAlreadyUsedError(
                    'Task already has student attempts and '
                    'cannot be changed safely.'
                )

            section = await self.uow.sections.get_by_id(task.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')

            section.remove_task(task.id)
            await self.uow.sections.update(section)
            await self.uow.tasks.remove(task)
            await self.uow.commit()
