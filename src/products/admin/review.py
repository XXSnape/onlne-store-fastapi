from sqladmin import ModelView

from products.database import ReviewModel


class ReviewAdmin(ModelView, model=ReviewModel):
    column_list = [
        ReviewModel.user,
        ReviewModel.product,
        ReviewModel.rate,
    ]
