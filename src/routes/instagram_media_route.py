from fastapi import APIRouter, Depends, status
from ..services import InstagramService
from ..dtos import InstagramMediaResponseDTO

router = APIRouter(prefix="/instagram", tags=["Instagram Media"])

def get_instagram_service() -> InstagramService:
    return InstagramService()

@router.get("/media", response_model=list[InstagramMediaResponseDTO], status_code=status.HTTP_200_OK)
def get_instagram_media(instagram_service: InstagramService = Depends(get_instagram_service)):
    return instagram_service.get_media()