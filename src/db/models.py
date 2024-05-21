from sqlalchemy import Column, Integer, Boolean, String

from db.orm import Base


class UsersTable(Base):
    __tablename__ = "users"

    id_number = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    is_admin = Column("is_admin", Boolean, nullable=False)


class TasksTable(Base):
    __tablename__ = "tasks"

    id_number = Column("id", Integer, primary_key=True)
    description = Column("description", String, nullable=False)
    priority = Column("priority", Integer)
    is_complete = Column("is_complete", Boolean)
