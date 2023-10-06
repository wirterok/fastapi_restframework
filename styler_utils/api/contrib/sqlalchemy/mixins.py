from fastapi import HTTPException

class ListMixin:
    async def list(self):
        return (await self.session.scalars(self.get_list_query())).all()


class CreateMixin:
    async def create(self):
        return
        return (await self.session.scalars(self.get_list_query())).all()


class RetriveMixin:
    async def retrieve(self):
        return await self.get_obj()


class DeleteMixin:
    async def delete(self):
        pass


class UpdateMixin:
    async def update(self):
        pass