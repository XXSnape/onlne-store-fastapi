from core import ManagerRepository
from users.database import UserModel


class UserRepository(ManagerRepository):
    model = UserModel
