from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)

class EventMapping(Base):
    __tablename__ = "event_mappings"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, index=True)
    provider_event_id = Column(String, index=True)
    internal_event_id = Column(String, index=True)
    last_sync = Column(DateTime, default=datetime.utcnow)
