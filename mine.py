from sqlalchemy import (Table, Column, Integer, String, create_engine,
    MetaData, ForeignKey)
from sqlalchemy.orm import mapper, create_session
from sqlalchemy.ext.declarative import declarative_base

e = create_engine('sqlite:///sqlite.db', echo=True)
Base = declarative_base(bind=e)

class Image(Base):
    def __init__(self, filename):
        self.filename = filename


    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(50))
    type = Column(String(30), nullable=False)

    __mapper_args__ = {'polymorphic_on': type}

    

class Student(Image):
    __tablename__ = 'students'
    __mapper_args__ = {'polymorphic_identity': 'student'}
    id = Column(Integer, primary_key=True, autoincrement=True)

    image_id = Column(Integer, ForeignKey('images.image_id'))
    student_name = Column(String(50))

    def __init__(self, filename, student_name):
        super(Student,self).__init__(filename)
        self.student_name = student_name

class Teacher(Image):
    __tablename__ = 'teachers'
    __mapper_args__ = {'polymorphic_identity': 'teacher'}
    id = Column(Integer, primary_key=True, autoincrement=True)

    image_id = Column(Integer, ForeignKey('images.image_id'))
    teacher_name = Column(String(50))

    def __init__(self, filename, teacher_name):
        super(Teacher,self).__init__(filename)
        self.teacher_name = teacher_name



Base.metadata.drop_all()
Base.metadata.create_all()

db_session = create_session(bind=e, autoflush=True, autocommit=False)  

student = Student("images/muqeet.png","Muqeet")
teacher = Teacher("images/ali_sher324.png","Ali Sher")

db_session.add(student)
db_session.add(teacher)
db_session.commit()