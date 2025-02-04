from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class ImageModelMixin:
    _directory: str | None = None

    @declared_attr
    def src(cls) -> Mapped[str]:
        return mapped_column(
            ImageType(
                storage=FileSystemStorage(path=f"uploads/{cls._directory}")
            )
        )

    @hybrid_property
    def alt(self) -> str:
        filename = self.src.split("/")[-1].split("_")[-1]
        return filename
