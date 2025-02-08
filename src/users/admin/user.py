from sqladmin import ModelView

from core import UUIDFilenameAdminMixin
from users.database import AvatarModel, UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.fullname,
        UserModel.username,
        UserModel.email,
        UserModel.is_admin,
    ]
    column_details_exclude_list = [UserModel.password]
    can_edit = False
    can_delete = False


class AvatarAdmin(UUIDFilenameAdminMixin, ModelView, model=AvatarModel):
    column_list = "__all__"
