from fastapi import APIRouter, Depends, status
from ..services import PromotionService
from ..repositories import PromotionRepository
from ..config import get_session
from sqlmodel import Session
from ..dtos import PromotionResponseDTO, CreatePromotionDTO, UpdatePromotionDTO
from ..utils.auth_dependency import authorization_header, current_user
from ..models import User

def get_promotion_service(session: Session = Depends(get_session)) -> PromotionService:
    return PromotionService(PromotionRepository(session))

router = APIRouter(prefix="/promotions", tags=["Promotions"])

@router.get("/", response_model=list[PromotionResponseDTO], status_code=status.HTTP_200_OK)
def get_promotions(promotion_service: PromotionService = Depends(get_promotion_service),
     auth: dict = Depends(authorization_header)
     ):
    return promotion_service.get_all_promotions()

@router.get("/{id}", response_model=PromotionResponseDTO, status_code=status.HTTP_200_OK)
def get_promotion_by_id(id: int, promotion_service: PromotionService = Depends(get_promotion_service), 
    auth: dict = Depends(authorization_header)):
    return promotion_service.get_promotion_by_id(id)

@router.post("/", response_model=PromotionResponseDTO, status_code=status.HTTP_201_CREATED)
def create_promotion(promotion_dto: CreatePromotionDTO, promotion_service: PromotionService = Depends(get_promotion_service),
     auth: dict = Depends(authorization_header),
     user: User = Depends(current_user)):
    return promotion_service.create_promotion(promotion_dto, current_user=user.email)

@router.put("/{id}", response_model=PromotionResponseDTO, status_code=status.HTTP_200_OK)
def update_promotion(promotion_dto: UpdatePromotionDTO, promotion_service: PromotionService = Depends(get_promotion_service), 
    auth: dict = Depends(authorization_header),
    user: User = Depends(current_user)):
    return promotion_service.update_promotion(promotion_dto, current_user=user.email)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(id: int, promotion_service: PromotionService = Depends(get_promotion_service),
     auth: dict = Depends(authorization_header)):
    return promotion_service.delete_promotion(id)