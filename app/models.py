# models.py
# SQLAlchemy models for OpenElectionsKe
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class County(Base):
    __tablename__ = 'counties'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    constituencies = relationship('Constituency', back_populates='county')

class Constituency(Base):
    __tablename__ = 'constituencies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    county_id = Column(Integer, ForeignKey('counties.id'))
    county = relationship('County', back_populates='constituencies')
    wards = relationship('Ward', back_populates='constituency')

class Ward(Base):
    __tablename__ = 'wards'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    constituency_id = Column(Integer, ForeignKey('constituencies.id'))
    constituency = relationship('Constituency', back_populates='wards')
    polling_stations = relationship('PollingStation', back_populates='ward')

class PollingStation(Base):
    __tablename__ = 'polling_stations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    code = Column(String(32), unique=True, nullable=True)
    ward_id = Column(Integer, ForeignKey('wards.id'))
    ward = relationship('Ward', back_populates='polling_stations')
    results = relationship('Result', back_populates='polling_station')

class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)
    level = Column(String(32), nullable=False)  # 'ward', 'constituency', 'county', 'national'
    candidates = relationship('Candidate', back_populates='position')
    results = relationship('Result', back_populates='position')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Election(Base):
    __tablename__ = 'elections'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    creator = relationship('User')

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    election_id = Column(Integer, ForeignKey('elections.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    election = relationship('Election')
    position = relationship('Position', back_populates='candidates')

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey('elections.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    polling_station_id = Column(Integer, ForeignKey('polling_stations.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))
    votes = Column(Integer, default=0)
    reported_at = Column(DateTime, default=datetime.datetime.utcnow)
    election = relationship('Election')
    candidate = relationship('Candidate')
    polling_station = relationship('PollingStation', back_populates='results')
    position = relationship('Position', back_populates='results')
