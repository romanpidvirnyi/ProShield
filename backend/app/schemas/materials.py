from pydantic import BaseModel


class MaterialCreate(BaseModel):
    name: str


class Material(MaterialCreate):
    id: int


class MaterialUpdate(MaterialCreate):
    pass
