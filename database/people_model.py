from pydantic import BaseModel


class PersonModel(BaseModel):
    name: str
    surname: str
    second_surname: str | None
