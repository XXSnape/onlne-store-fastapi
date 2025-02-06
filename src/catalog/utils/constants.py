import enum


class SortingEnum(enum.StrEnum):
    rating = "rating"
    price = "price"
    reviews = "reviews"
    date = "date"


class SortingTypeEnum(enum.StrEnum):
    inc = "inc"
    dec = "dec"
