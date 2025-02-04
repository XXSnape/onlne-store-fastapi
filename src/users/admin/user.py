from sqladmin import ModelView

from core import UUIDFilenameAdminMixin
from users.database import UserModel, AvatarModel


class UserAdmin(ModelView, model=UserModel):
    column_list = "__all__"
    column_details_exclude_list = [UserModel.password]
    can_edit = False
    can_delete = False


class AvatarAdmin(UUIDFilenameAdminMixin, ModelView, model=AvatarModel):
    column_list = "__all__"
