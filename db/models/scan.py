from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ScanTask(Base):
    __tablename__ = "scan_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(64), unique=True, nullable=False, index=True)
    target = Column(String(256), nullable=False)
    status = Column(String(32), default="pending")  # pending / running / completed / failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_raw_items = Column(Integer, default=0)
    total_iocs = Column(Integer, default=0)
    total_verified = Column(Integer, default=0)
    report_path = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)

class IntelligenceRecord(Base):
    __tablename__ = "intelligence_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_task_id = Column(String(64), nullable=False, index=True)
    source = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(128), nullable=True)
    image_url = Column(String(512), nullable=True)
    confidence_score = Column(Float, default=0.0)
    verified = Column(Boolean, default=False)
    iocs = Column(JSON, default=list)
    ttps = Column(JSON, default=list)
    enrichment = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

class ThreatActor(Base):
    __tablename__ = "threat_actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False, index=True)
    aliases = Column(JSON, default=list)
    origin_country = Column(String(64), nullable=True)
    motivation = Column(String(128), nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    associated_malware = Column(JSON, default=list)
    mitre_groups = Column(JSON, default=list)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
