from abc import ABC, abstractmethod
from ...dtos import UpdateAppointmentDTO
from typing import Any


class Promotion(ABC):
    @abstractmethod
    def apply(self, appointment: UpdateAppointmentDTO) -> UpdateAppointmentDTO:
        pass
