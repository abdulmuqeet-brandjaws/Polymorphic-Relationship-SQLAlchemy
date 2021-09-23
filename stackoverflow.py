from sqlalchemy import (Table, Column, Integer, String, create_engine,
    MetaData, ForeignKey)
from sqlalchemy.orm import mapper, create_session
from sqlalchemy.ext.declarative import declarative_base

e = create_engine('sqlite:///sqlite.db', echo=True)
Base = declarative_base(bind=e)

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(30), nullable=False)

    __mapper_args__ = {'polymorphic_on': type}

    def __init__(self, name):
        self.name = name

class Manager(Employee):
    __tablename__ = 'managers'
    __mapper_args__ = {'polymorphic_identity': 'manager'}

    employee_id = Column(Integer, ForeignKey('employees.employee_id'),
        primary_key=True)
    manager_data = Column(String(50))

    def __init__(self, name, manager_data):
        super(Manager, self).__init__(name)
        self.manager_data = manager_data

class Owner(Manager):
    __tablename__ = 'owners'
    __mapper_args__ = {'polymorphic_identity': 'owner'}

    employee_id = Column(Integer, ForeignKey('managers.employee_id'),
        primary_key=True)
    owner_secret = Column(String(50))

    def __init__(self, name, manager_data, owner_secret):
        super(Owner, self).__init__(name, manager_data)
        self.owner_secret = owner_secret

Base.metadata.drop_all()
Base.metadata.create_all()

db_session = create_session(bind=e, autoflush=True, autocommit=False)    
o = Owner('nosklo', 'mgr001', 'ownerpwd')

db_session.add(o)
db_session.commit()