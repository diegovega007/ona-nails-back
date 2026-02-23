from fastapi import APIRouter, Depends, status

from ..services import GalleryService, CloudinaryService
from ..dtos import GalleryResponseDTO, CreateGalleryDTO, UpdateGalleryDTO
from fastapi import UploadFile, File
from ..repositories import GalleryRepository
from ..config import get_session
from ..utils.auth_dependency import authorization_header
from sqlmodel import Session

def get_gallery_service(session: Session = Depends(get_session)) -> GalleryService:
    return GalleryService(GalleryRepository(session), CloudinaryService())

router = APIRouter(prefix="/galleries", tags=["Galleries"])

@router.post("/", response_model=GalleryResponseDTO, status_code=status.HTTP_201_CREATED)
def create_gallery(
file: UploadFile = File(...), 
create_gallery_dto: CreateGalleryDTO = Depends(CreateGalleryDTO), 
gallery_service: GalleryService = Depends(get_gallery_service), auth: dict = Depends(authorization_header)):
    return gallery_service.create_gallery(file, create_gallery_dto)

@router.get("/", response_model=list[GalleryResponseDTO], status_code=status.HTTP_200_OK)
def get_all_galleries(gallery_service: GalleryService = Depends(get_gallery_service), auth: dict = Depends(authorization_header)):
    return gallery_service.get_all_galleries()

@router.get("/{id}", response_model=GalleryResponseDTO, status_code=status.HTTP_200_OK)
def get_gallery_by_id(id: int, gallery_service: GalleryService = Depends(get_gallery_service), auth: dict = Depends(authorization_header)):
    return gallery_service.get_gallery_by_id(id)

@router.put("/", response_model=GalleryResponseDTO, status_code=status.HTTP_200_OK)
def update_gallery(file: UploadFile = File(...), update_gallery_dto: UpdateGalleryDTO = Depends(UpdateGalleryDTO), gallery_service: GalleryService = Depends(get_gallery_service), auth: dict = Depends(authorization_header)):
    return gallery_service.update_gallery(file, update_gallery_dto)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_galleries(ids: list[int], gallery_service: GalleryService = Depends(get_gallery_service), auth: dict = Depends(authorization_header)):
    return gallery_service.delete_galleries(ids)