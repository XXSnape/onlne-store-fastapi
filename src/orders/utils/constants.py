import enum


class DeliveryTypeEnum(enum.StrEnum):
    ordinary = "ordinary"
    express = "express"


class PaymentTypeEnum(enum.StrEnum):
    online = "online"
    someone = "someone"


class OrderStatusEnum(enum.StrEnum):
    unpaid = "unpaid"
    paid = "paid"
