from cloudinary.uploader import upload
from cloudinary.api import delete_resources
from cloudinary.utils import cloudinary_url
from ..exeptions import CloudinaryException

class CloudinaryService:

    def get_resource(self, public_id: str) -> str:
        data = cloudinary_url(public_id)
        if data.get("error"):
            raise CloudinaryException(data.get("error").get("message"))
        return data

    def get_resources(self, public_ids: list[str]) -> list[str]:
        resources = []
        for public_id in public_ids:
            data = cloudinary_url(public_id)
            if data.get("error"):
                raise CloudinaryException(data.get("error").get("message"))
            resources.append(data)
        return resources

    def upload(self, resource: str) -> str:
        data = upload(resource, resource_type="auto")
        if data.get("error"):
            raise CloudinaryException(data.get("error").get("message"))
        return data

    def delete(self, public_ids: list[str]) -> bool:
        data = delete_resources(public_ids)
        if data.get("error"):
            raise CloudinaryException(data.get("error").get("message"))
        return data

