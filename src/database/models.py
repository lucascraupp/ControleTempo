from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[Integer] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(50), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    areas_of_life: Mapped[List["AreasOfLife"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    projects: Mapped[List["Projects"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    tasks: Mapped[List["Tasks"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    projects_areas: Mapped[List["ProjectsHasAreasOfLife"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    user_tasks: Mapped[List["UsersHasTasks"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class AreasOfLife(Base):
    __tablename__ = "areas_of_life"

    id: Mapped[Integer] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(100), nullable=False)
    who_created: Mapped[Integer] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="areas_of_life")
    projects_areas: Mapped[List["ProjectsHasAreasOfLife"]] = relationship(
        back_populates="area_of_life", cascade="all, delete-orphan"
    )
    tasks_areas: Mapped[List["TasksHasAreasOfLife"]] = relationship(
        back_populates="area_of_life", cascade="all, delete-orphan"
    )


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[Integer] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(100), nullable=False)
    who_created: Mapped[Integer] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="projects")
    projects_areas: Mapped[List["ProjectsHasAreasOfLife"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[Integer] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(100), nullable=False)
    who_created: Mapped[Integer] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="tasks")
    task_users: Mapped[List["UsersHasTasks"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )


class ProjectsHasAreasOfLife(Base):
    __tablename__ = "projects_has_areas_of_life"

    user_id: Mapped[Integer] = mapped_column(ForeignKey("users.id"), primary_key=True)
    area_of_life_id: Mapped[Integer] = mapped_column(
        ForeignKey("areas_of_life.id"), primary_key=True
    )
    project_id: Mapped[Integer] = mapped_column(
        ForeignKey("projects.id"), primary_key=True
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="projects_areas")
    area_of_life: Mapped["AreasOfLife"] = relationship(back_populates="projects_areas")
    project: Mapped["Projects"] = relationship(back_populates="projects_areas")
    tasks_projects: Mapped[List["TasksHasProjects"]] = relationship(
        back_populates="project_area", cascade="all, delete-orphan"
    )


class UsersHasTasks(Base):
    __tablename__ = "users_has_tasks"

    user_id: Mapped[Integer] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[Integer] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="user_tasks")
    task: Mapped["Tasks"] = relationship(back_populates="task_users")
    tasks_areas: Mapped[List["TasksHasAreasOfLife"]] = relationship(
        back_populates="task_user", cascade="all, delete-orphan"
    )
    tasks_projects: Mapped[List["TasksHasProjects"]] = relationship(
        back_populates="task_user", cascade="all, delete-orphan"
    )


class TasksHasAreasOfLife(Base):
    __tablename__ = "tasks_has_areas_of_life"

    user_id: Mapped[Integer] = mapped_column(
        ForeignKey("users_has_tasks.user_id"), primary_key=True
    )
    task_id: Mapped[Integer] = mapped_column(
        ForeignKey("users_has_tasks.task_id"), primary_key=True
    )
    area_of_life_id: Mapped[Integer] = mapped_column(
        ForeignKey("areas_of_life.id"), primary_key=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    task_user: Mapped["UsersHasTasks"] = relationship(back_populates="tasks_areas")
    area_of_life: Mapped["AreasOfLife"] = relationship(back_populates="tasks_areas")


class TasksHasProjects(Base):
    __tablename__ = "tasks_has_projects"

    user_id: Mapped[Integer] = mapped_column(
        ForeignKey("users_has_tasks.user_id"), primary_key=True
    )
    task_id: Mapped[Integer] = mapped_column(
        ForeignKey("users_has_tasks.task_id"), primary_key=True
    )
    area_of_life_id: Mapped[Integer] = mapped_column(
        ForeignKey("projects_has_areas_of_life.area_of_life_id"), primary_key=True
    )
    project_id: Mapped[Integer] = mapped_column(
        ForeignKey("projects_has_areas_of_life.project_id"), primary_key=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    task_user: Mapped["UsersHasTasks"] = relationship(back_populates="tasks_projects")
    project_area: Mapped["ProjectsHasAreasOfLife"] = relationship(
        back_populates="tasks_projects"
    )
