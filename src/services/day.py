from src.repositories import DayRepository
from src.exceptions import NotFoundException
from src.schemas import DayRead, DayCreate, DayUpdate


class DayService:
    def __init__(self, day_repository: DayRepository):
        self.day_repository = day_repository

    def get_day(self, day_id: int) -> DayRead:
        day = self.day_repository.get_day(day_id)
        if not day:
            raise NotFoundException(day_id)
        return day

    def create_day(self, day_data: DayCreate) -> DayRead:
        return self.day_repository.create_day(day_data)

    def update_day(self, day_id: int, day_update: DayUpdate) -> DayRead:
        day = self.day_repository.get_day(day_id)
        if not day:
            raise NotFoundException(day_id)

        update_data = day_update.model_dump(exclude_unset=True)
        self.day_repository.update_day(day_id, update_data)

        return self.day_repository.get_day(day_id)

    def delete_day(self, day_id: int) -> DayRead:
        day = self.day_repository.get_day(day_id)
        if not day:
            raise NotFoundException(day_id)

        self.day_repository.delete_day(day_id)
        return day
