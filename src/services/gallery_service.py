from ..repositories import GalleryRepository
from .cloudinary_service import CloudinaryService
from ..dtos import  GalleryResponseDTO, CreateGalleryDTO, UpdateGalleryDTO
from ..models import Gallery
from ..exeptions import GalleryNotFound
from fastapi import UploadFile
from datetime import datetime

class GalleryService:
    def __init__(self, gallery_repository: GalleryRepository, cloudinary_service: CloudinaryService):
        self.gallery_repository = gallery_repository
        self.cloudinary_service = cloudinary_service

    def get_all_galleries(self) -> list[GalleryResponseDTO]:
        galleries = self.gallery_repository.get_all()
        return [GalleryResponseDTO.model_validate(gallery) for gallery in galleries]
    
    def get_gallery_by_id(self, id: int) -> GalleryResponseDTO:
        gallery = self.gallery_repository.get_by_id(id)
        if not gallery:
            raise GalleryNotFound()
        return GalleryResponseDTO.model_validate(gallery)

    def create_gallery(self, file: UploadFile, create_gallery_dto: CreateGalleryDTO) -> GalleryResponseDTO:
        gallery = self.cloudinary_service.upload(file.file)
        gallery = self.gallery_repository.create(
            Gallery(url=gallery.get("url"), public_id=gallery.get("public_id"), type=create_gallery_dto.type, created_at=datetime.now()) 
        )
        return GalleryResponseDTO.model_validate(gallery)

    def update_gallery(self, file: UploadFile, update_gallery_dto: UpdateGalleryDTO) -> GalleryResponseDTO:
        gallery = self.gallery_repository.get_by_id(update_gallery_dto.id)
        if not gallery:
            raise GalleryNotFound()
        self.cloudinary_service.delete([gallery.public_id])
        gallery = self.cloudinary_service.upload(file.file)
        gallery = self.gallery_repository.update(
            Gallery(**update_gallery_dto.model_dump(), url=gallery.get("url"), public_id=gallery.get("public_id"), modified_at=datetime.now())
        )
        return GalleryResponseDTO.model_validate(gallery)

    def delete_galleries(self, ids: list[int]) -> bool:
        galleries = self.gallery_repository.get_by_ids(ids)
        if not galleries:
            raise GalleryNotFound()
        self.cloudinary_service.delete([gallery.public_id for gallery in galleries])
        return self.gallery_repository.delete_by_ids(ids)
    