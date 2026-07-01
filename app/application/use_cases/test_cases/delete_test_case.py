from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import (
    TestCaseNotFoundError,
    CodeTaskNotFoundError,
    CodeTaskAlreadyUsedError,
    CodeTaskInvalidConfigurationError
)
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User


@dataclass(slots=True)
class DeleteTestCaseCommand:
    actor: User
    test_case_id: UUID


class DeleteTestCaseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteTestCaseCommand) -> None:
        async with self.uow:
            test_case = await self.uow.test_cases.get_by_id(
                command.test_case_id
            )
            if test_case is None:
                raise TestCaseNotFoundError('Test case not found.')

            code_task = await self.uow.code_tasks.get_by_id(
                test_case.code_task_id
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

            code_task.remove_test_case(test_case.id)

            if not code_task.test_case_ids:
                raise CodeTaskInvalidConfigurationError(
                    'Code task must keep at least one test case.'
                )
            await self.uow.code_tasks.update(code_task)
            await self.uow.test_cases.remove(test_case)
            await self.uow.commit()
