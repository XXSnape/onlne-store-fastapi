from core import ManagerRepository
from users.database import AvatarModel


class AvatarRepository(ManagerRepository):
    model = AvatarModel
