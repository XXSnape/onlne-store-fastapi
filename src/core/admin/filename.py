import uuid


class UUIDFilenameAdminMixin:
    async def insert_model(self, request, data):
        data["src"].filename = f"{uuid.uuid4()}_{data['src'].filename}"
        return await super().insert_model(request, data)
