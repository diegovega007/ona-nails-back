from abc import ABC, abstractmethod
from ...dtos import UpdateAppointmentDTO


class Promotion(ABC):
    @abstractmethod
    def apply(self, appointment: UpdateAppointmentDTO) -> UpdateAppointmentDTO:
        pass
