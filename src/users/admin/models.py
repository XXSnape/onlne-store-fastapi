from sqladmin import ModelView
from users.database import UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.fullname,
        UserModel.email,
        UserModel.phone,
        UserModel.username,
        UserModel.is_admin,
    ]
    column_details_exclude_list = [UserModel.password]
    can_edit = False
    can_delete = False
