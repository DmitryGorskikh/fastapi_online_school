from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import (
    CourseNotFoundError
)
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteCourseCommand:
    course_id: UUID


class DeleteCourseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, command: DeleteCourseCommand
    ) -> None:
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if course is None:
                raise CourseNotFoundError("Course not found.")

            modules = await self.uow.modules.get_by_ids(course.module_ids)
            for module in modules:
                sections = await self.uow.sections.get_by_ids(
                    module.section_ids
                )
                for section in sections:
                    lectures = await self.uow.lectures.get_by_ids(
                        section.lecture_ids
                    )
                    for lecture in lectures:
                        await self.uow.lectures.remove(lecture)
                    await self.uow.sections.remove(section)
                await self.uow.modules.remove(module)

            await self.uow.courses.remove(course)
            await self.uow.commit()
