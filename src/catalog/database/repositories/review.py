from catalog.database import ReviewModel
from core import ManagerRepository


class ReviewRepository(ManagerRepository):
    model = ReviewModel
