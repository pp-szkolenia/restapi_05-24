from sqlalchemy import Column, Integer, Boolean, String

from db.orm import Base


class UsersTable(Base):
    __tablename__ = "users"

    id_number = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    is_admin = Column("is_admin", Boolean, nullable=False)
