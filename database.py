from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    turns = Column(Integer)
    cheat_mode = Column(Boolean)
    duplicate_color = Column(Boolean)
    number_of_colors = Column(Integer)
    number_of_positions = Column(Integer)


class Pin(Base):
    __tablename__ = 'pin'
    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    game = relationship(Game)
    color = Column(String, ForeignKey('pincolor.color'))
    x = Column(Integer, primary_key=True)
    y = Column(Integer, primary_key=True)


class PinColor(Base):
    __tablename__ = 'pincolor'
    color = Column(String, primary_key=True)


engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)
