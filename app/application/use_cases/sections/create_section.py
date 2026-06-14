from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import ModuleNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities import User
from app.domain.entities.section import Section


@dataclass(slots=True)
class CreateSectionCommand:
    author: User
    module_id: UUID
    title: str
    description: str
    position: int


class CreateSectionUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: CreateSectionCommand) -> Section:
        async with self.uow:
            module = await self.uow.modules.get_by_id(command.module_id)
            if module is None:
                raise ModuleNotFoundError('Module not found.')

            await self.course_access_service.ensure_can_manage_module(
                author=command.author,
                module_id=module.id,
            )

            section = Section(
                id=uuid4(),
                module_id=command.module_id,
                title=command.title,
                description=command.description,
                position=command.position,
            )
            module.add_section(section.id)
            await self.uow.sections.add(section)
            await self.uow.modules.update(module)
            await self.uow.commit()
            return section
