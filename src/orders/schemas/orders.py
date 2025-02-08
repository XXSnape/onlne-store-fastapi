from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

from catalog.schemas.products import ProductGeneralSchema
from orders.utils.constants import DeliveryTypeEnum, PaymentTypeEnum


class OrderInSchema(BaseModel):
    id: int
    created_at: Annotated[datetime, Field(validation_alias="createdAt")]
    fullname: Annotated[str, Field(validation_alias="fullName")]
    email: str
    phone: str
    delivery_type: Annotated[
        DeliveryTypeEnum, Field(validation_alias="deliveryType")
    ]
    payment_type: Annotated[
        PaymentTypeEnum, Field(validation_alias="paymentType")
    ]
    total_cost: Annotated[Decimal, Field(validation_alias="totalCost")]
    status: str
    city: str
    address: str
    products: list[ProductGeneralSchema]


class OrdersSchema(OrderInSchema):
    created_at: Annotated[datetime, Field(serialization_alias="createdAt")]
    fullname: Annotated[str, Field(serialization_alias="fullName")]
    email: str
    phone: str
    delivery_type: Annotated[
        DeliveryTypeEnum | None, Field(serialization_alias="deliveryType")
    ]
    payment_type: Annotated[
        PaymentTypeEnum | None, Field(serialization_alias="paymentType")
    ]
    total_cost: Annotated[
        Decimal | None, Field(serialization_alias="totalCost")
    ]


class OrderIdOutSchema(BaseModel):
    order_id: Annotated[int, Field(serialization_alias="orderId")]
