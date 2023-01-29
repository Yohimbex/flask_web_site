from peewee import CharField
from flask_login import UserMixin

from app.base_model import BaseModel


class AuthUser(UserMixin, BaseModel):
    email = CharField(max_length=150, unique=True, index=True)
    password = CharField(max_length=100, null=True)
    name = CharField(max_length=100, null=True)
