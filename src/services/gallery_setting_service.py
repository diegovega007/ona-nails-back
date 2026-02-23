from ..repositories import GallerySettingRepository
from ..dtos import GallerySettingDTO
from datetime import datetime
from ..models import GallerySetting

class GallerySettingService:
    def __init__(self, gallery_setting_repository: GallerySettingRepository):
        self.gallery_setting_repository = gallery_setting_repository

    def get_gallery_setting(self) -> GallerySettingDTO:
        gallery_setting = self.gallery_setting_repository.get_by_id(1)
        return GallerySettingDTO.model_validate(gallery_setting)

    def update_gallery_setting(self, gallery_setting_dto: GallerySettingDTO) -> GallerySettingDTO:
        gallery_setting = self.gallery_setting_repository.update(
            GallerySetting(**gallery_setting_dto.model_dump(), modified_at=datetime.now(), id=1)
        )
        return GallerySettingDTO.model_validate(gallery_setting)