from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import (
    QuestionAlreadyUsedError,
    QuestionNotFoundError,
    SectionNotFoundError,
    AnswerOptionNotFoundError
)
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.answer_option import AnswerOption
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.user import User


@dataclass(slots=True)
class DeleteAnswerOptionCommand:
    actor: User
    answer_option_id: UUID


class DeleteAnswerOptionUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(
        self, command: DeleteAnswerOptionCommand
    ) -> AnswerOption:
        async with self.uow:
            answer_option = await self.uow.answer_options.get_by_id(
                command.answer_option_id
            )
            if answer_option is None:
                raise AnswerOptionNotFoundError(
                    'Answer option not found.'
                )

            question = await self.uow.questions.get_by_id(
                answer_option.question_id
            )
            if question is None:
                raise QuestionNotFoundError(
                    'Question option not found.'
                )

            section = await self.uow.sections.get_by_id(question.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')

            await self.course_access_service.ensure_can_manage_section(
                actor=command.actor,
                section_id=section.id,
            )

            has_attempts = await (
                self.uow.question_attempts.exists_by_question_id(question.id)
            )
            if has_attempts:
                raise QuestionAlreadyUsedError(
                    'Question already has student attempts and '
                    'cannot be changed safely.'
                )

            question.remove_answer_option(answer_option.id)
            await self.uow.questions.update(question)
            await self.uow.answer_options.remove(answer_option)
            await self.uow.commit()
