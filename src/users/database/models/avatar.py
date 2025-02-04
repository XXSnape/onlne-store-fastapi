from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from core import BaseModel
from .mixins.user import UserRelationshipMixin


class AvatarModel(UserRelationshipMixin, BaseModel):
    _is_unique_user = True
    _back_populates = "avatar"

    src: Mapped[str] = mapped_column(
        ImageType(storage=FileSystemStorage(path="uploads/avatars"))
    )

    @hybrid_property
    def alt(self) -> str:
        filename = self.src.split("/")[-1]
        return f"{self.user_id}_{filename}"
