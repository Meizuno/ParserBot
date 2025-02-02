from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from src.config import DB_URL

engine = create_engine(DB_URL)


class ParsedURL(SQLModel, table=True):
    """Parsed URL model"""

    __tablename__ = "parsed_url"

    id: int = Field(default=None, primary_key=True, index=True)
    url: str = Field(max_length=255)
    key: str = Field(max_length=255)
    is_active: bool = Field(default=True)

    def create(self) -> "ParsedURL":
        """Create new parsed url"""

        with Session(engine) as session:
            session.add(self)
            session.commit()
            session.refresh(self)

        return self

    @classmethod
    def all(cls) -> list["ParsedURL"]:
        """Get all parsed urls"""

        with Session(engine) as session:
            return session.exec(select(cls).where(cls.is_active)).all()


class ParsedItem(SQLModel, table=True):
    """Parsed Item model"""

    __tablename__ = "parsed_item"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    url: int = Field(foreign_key="parsed_url.id")
    result: str = Field(max_length=1000)

    @classmethod
    def exists(cls, url: str, result: str) -> bool:
        """Check if parsed item exists"""

        with Session(engine) as session:
            return session.exec(
                select(cls).where(cls.url == url and cls.result == result)
            ).first() is not None

    @classmethod
    def create(cls, url: str, result: str) -> "ParsedItem":
        """Create new parsed item"""

        with Session(engine) as session:
            instance = cls(url=url, result=result)
            session.add(instance)
            session.commit()
            session.refresh(instance)

        return instance
