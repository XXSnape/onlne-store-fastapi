from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


def get_filename(path: str):
    return path.split("/")[-1].split("_")[-1]


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
        filename = get_filename(self.src)
        return filename

    def __repr__(self) -> str:
        filename = get_filename(self.src)
        return f"{self._directory}/{filename}"
