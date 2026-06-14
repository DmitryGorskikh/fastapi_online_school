from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities import User
from app.domain.entities.lecture import Lecture


@dataclass(slots=True)
class CreateLectureCommand:
    author: User
    section_id: UUID
    title: str
    content: str
    position: int


class CreateLectureUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: CreateLectureCommand) -> Lecture:
        async with self.uow:
            section = await self.uow.sections.get_by_id(command.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')

            await self.course_access_service.ensure_can_manage_section(
                author=command.author,
                section_id=section.id,
            )

            lecture = Lecture(
                id=uuid4(),
                section_id=command.section_id,
                title=command.title,
                content=command.content,
                position=command.position,
            )
            section.add_lecture(lecture.id)
            await self.uow.lectures.add(lecture)
            await self.uow.sections.update(section)
            await self.uow.commit()
            return lecture
