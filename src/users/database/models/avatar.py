from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from core import BaseModel
from .mixins.user import UserRelationshipMixin


class AvatarModel(UserRelationshipMixin, BaseModel):
    _is_unique_user = True
    _back_populates = "avatar"
    src: Mapped[str]

    @hybrid_property
    def alt(self) -> str:
        filename = self.src.split("/")[-1]
        return f"{self.user_id}_{filename}"
