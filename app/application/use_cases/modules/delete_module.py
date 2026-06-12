from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import (
    ModuleNotFoundError, CourseNotFoundError
)
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteModuleCommand:
    module_id: UUID


class DeleteModuleUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, command: DeleteModuleCommand
    ) -> None:
        async with self.uow:
            module = await self.uow.modules.get_by_id(command.module_id)
            if module is None:
                raise ModuleNotFoundError("Module not found.")

            course = await self.uow.courses.get_by_id(module.course_id)
            if course is None:
                raise CourseNotFoundError("Course not found.")

            sections = await self.uow.sections.get_by_ids(module.section_ids)
            for section in sections:
                lectures = await self.uow.lectures.get_by_ids(
                    section.lecture_ids
                )
                for lecture in lectures:
                    await self.uow.lectures.remove(lecture)
                await self.uow.sections.remove(section)

            course.remove_module(module.id)
            await self.uow.courses.update(course)
            await self.uow.modules.remove(module)
            await self.uow.commit()
