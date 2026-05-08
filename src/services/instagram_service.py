from dotenv import load_dotenv
import os
from ..utils.meta.instagram import get_media
import asyncio
from ..dtos import InstagramMediaResponseDTO

load_dotenv()

class InstagramService:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.user_id = os.getenv("INSTAGRAM_USER_ID")
        self.url = f"https://graph.facebook.com/v19.0/{self.user_id}/media"

    def get_media(self) -> list[InstagramMediaResponseDTO]:
        media = asyncio.run(get_media(self.access_token, self.url))
        return [InstagramMediaResponseDTO.model_validate(item) for item in media]
    