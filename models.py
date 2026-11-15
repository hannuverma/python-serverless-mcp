from time import time
from enum import unique
from sqlalchemy.orm import Mapped
from sqlalchemy import true
from click import STRING
from datetime import datetime
from sqlalchemy import ARRAY, DECIMAL, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship


Base = declarative_base()

class Section(Base):
    __tablename__ = "section"

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    pages: Mapped[list["Page"]] = relationship("Page", back_populates="section", cascade="all, delete-orphan")
    personnel = Mapped[list["Personnel"]] = relationship("Personnel", back_populates="section", cascade="all, delete-orphan")

class Page(Base):
    __tablename__ = "page"
    id: Mapped[int] = mapped_column(Integer, unique=true, primary_key=true)
    section_id: Mapped[int] = mapped_column(Integer, ForeignKey("section.id", ondelete="CASCADE"), nullable=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    markdown_content: Mapped[str] = mapped_column(Text, nullable=False)

    section: Mapped["Section | None"] = relationship("Section", back_populates="pages")

class Personnel(Base):
    __tablename__ = "personnel"

    id: Mapped[int] = mapped_column(Integer, unique=true, primary_key=true)
    section: Mapped[list["Section"]] = relationship("Section", back_populates="pages")
    section_id: Mapped[int] = mapped_column(Integer, ForeignKey("section.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    designation: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    department: Mapped[str] = mapped_column(String(200), index=True)
    email: Mapped[str] = mapped_column(String(255))
    profile_image_url: Mapped[Text] = mapped_column(Text)
    bio: Mapped[Text] = mapped_column(Text)

    sectio: Mapped["Section | None"] = relationship("Section", back_populates="personnel")

class PlacementStats(Base):
    __tablename__ = "placement_stats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    batch_year: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    highest_package: Mapped[float] = mapped_column(DECIMAL(10, 2))
    average_package: Mapped[float] = mapped_column(DECIMAL(10, 2))
    placement_percentage: Mapped[float] = mapped_column(DECIMAL(5, 2))
    key_highlights: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
