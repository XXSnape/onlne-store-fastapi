from typing import Final

from core import BaseModel, ImageModelMixin
from .mixins.user import UserRelationshipMixin

DIRECTORY_OF_IMAGES: Final[str] = "avatars"


class AvatarModel(UserRelationshipMixin, ImageModelMixin, BaseModel):
    _directory = DIRECTORY_OF_IMAGES
    _is_unique_user = True
    _back_populates = "avatar"
