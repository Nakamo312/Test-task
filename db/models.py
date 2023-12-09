from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TextEntry(Base):
    __tablename__ = 'text_entries'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    title = Column(String)
    x_avg_count_in_line = Column(Float)
