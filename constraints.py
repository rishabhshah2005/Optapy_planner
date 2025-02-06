#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from domain import Lecture, Division
from optapy import constraint_provider, get_class
from optapy.constraint import Joiners
from optapy.score import HardSoftScore
from optapy.constraint import ConstraintFactory
from datetime import date
from datetime import time, datetime, timedelta


DivisionClass = get_class(Division)
LectureClass = get_class(Lecture)

today = date.today()


def within_30_minutes(lesson1: Lecture, lesson2: Lecture):
    between = datetime.combine(today, lesson1.timeslot.end_time) - datetime.combine(today, lesson2.timeslot.start_time)
    return timedelta(minutes=0) == between


def room_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, room, teacher, subject, timeslot=None, division=None)
    a = constraint_factory. \
        forEach(LectureClass). \
            join(LectureClass, 
                     Joiners.equal(lambda l: l.timeslot),
                     Joiners.equal(lambda l: l.room),
                     Joiners.less_than(lambda l: l.id),
                 ).penalize("room conflict", HardSoftScore.ONE_HARD)
    return a

def teacher_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, room, teacher, subject, timeslot=None, division=None)
    a = constraint_factory. \
        forEach(LectureClass). \
            join(LectureClass, 
                 [
                     Joiners.equal(lambda l: l.timeslot),
                     Joiners.equal(lambda l: l.teacher),
                     Joiners.less_than(lambda l: l.id),
                 ]).penalize("teacher conflict", HardSoftScore.ONE_HARD)
    return a
    
def class_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, room, teacher, subject, timeslot=None, division=None)
    a = constraint_factory. \
        forEach(LectureClass). \
            join(LectureClass, 
                     Joiners.equal(lambda l: l.division),
                     Joiners.equal(lambda l: l.timeslot),
                     Joiners.less_than(lambda l: l.id),
                 ).penalize("Student group conflict", HardSoftScore.ONE_HARD)
    return a 
  
def same_classes_together(constraint_factory: ConstraintFactory):
    a = constraint_factory. \
        for_each(LectureClass). \
            join(LectureClass, 
                    Joiners.equal(lambda l: l.division),
                    Joiners.equal(lambda l: l.timeslot.day_of_week),
                    Joiners.less_than(lambda l: l.id),
                    Joiners.filtering(lambda a, b: within_30_minutes(a,b) and a.subject!=b.subject)
                 ) \
                     .penalize("same classes together", HardSoftScore.ONE_HARD)
    return a   

def check_time(a, b):
    a= a.timeslot.end_time
    b= b.timeslot.start_time
    return ((b.hour-a.hour)*60 + b.minute-a.minute)>0
    
@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        room_conflict(constraint_factory),
        class_conflict(constraint_factory),
        teacher_conflict(constraint_factory),
        same_classes_together(constraint_factory)
    ]
    