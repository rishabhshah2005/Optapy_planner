#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from domain import Lecture, Room
from optapy import constraint_provider, get_class
from optapy.constraint import Joiners
from optapy.score import HardSoftScore
from optapy.constraint import ConstraintFactory, ConstraintCollectors
from datetime import date
from datetime import time, datetime, timedelta


LectureClass = get_class(Lecture)
RoomClass = get_class(Room)

today = date.today()

lab_lectures=["FSD", "Python"]
room_lectures = ["DE", "PS"]

def diffisZero(lesson1: Lecture, lesson2: Lecture):
    between = datetime.combine(today, lesson1.timeslot.end_time) - datetime.combine(today, lesson2.timeslot.start_time)
    between2 = datetime.combine(today, lesson2.timeslot.end_time) - datetime.combine(today, lesson1.timeslot.start_time)
    
    return (timedelta(minutes=0) == between) or (timedelta(minutes=0) == between2)

def classAfterBreak(lesson1: Lecture, lesson2: Lecture):
    between = datetime.combine(today, lesson1.timeslot.end_time) - datetime.combine(today, lesson2.timeslot.start_time)
    if between.days<0:
        between = abs(between)
    return timedelta(minutes=45) == between <= timedelta(minutes=105)

def classJustAfterBreak(lesson1: Lecture, lesson2: Lecture):
    between = datetime.combine(today, lesson1.timeslot.end_time) - datetime.combine(today, lesson2.timeslot.start_time)
    if between.days<0:
        between = abs(between)
    return timedelta(minutes=45) == between

def isOverlapping(l1: Lecture, l2: Lecture):
    return l1.id!=l2.id and l1.teacher==l2.teacher and l1.subject==l2.subject and l1.division==l2.division \
            and l1.room==l2.room and l1.timeslot==l2.timeslot

# Rooms should not be same
def room_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    a = constraint_factory. \
        for_each_unique_pair(LectureClass,
                        Joiners.equal(lambda l1: l1.room),
                        Joiners.equal(lambda l1: l1.timeslot),
                             ) \
                 .penalize("room conflict", HardSoftScore.ONE_HARD)
    return a

def teacher_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    a = constraint_factory. \
        for_each_unique_pair(LectureClass,
                Joiners.equal(lambda l1: l1.teacher),
                Joiners.equal(lambda l1: l1.timeslot),
                )\
                .penalize("teacher conflict", HardSoftScore.ONE_HARD)
    return a

# Division conflict
def class_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    a = constraint_factory. \
        for_each_unique_pair(LectureClass, 
                             Joiners.equal(lambda l1: l1.division),
                             Joiners.equal(lambda l1: l1.timeslot)
                             )\
                 .penalize("class conflict", HardSoftScore.ONE_HARD)
    return a

# Each day should have 4 lectures for each division
def four_lectures_per_day(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(Lecture)
                              .group_by(lambda lecture: (lecture.timeslot.day_of_week, lecture.division),  # group into lectures on the same day
                                        ConstraintCollectors.count())  # count lectures in the group
                              .filter(lambda day_of_week, count: count != 4)
                              .penalize("four lectures per day", HardSoftScore.ONE_HARD)
    )

# Try to have consecutive classes of same subject
def same_rooms_together(constraint_factory: ConstraintFactory):
    a = constraint_factory. \
            for_each_unique_pair(LectureClass, 
                    Joiners.equal(lambda l: l.division),
                    Joiners.equal(lambda l: l.timeslot.day_of_week),
                    Joiners.filtering(lambda a, b: diffisZero(a,b) and (a.room!=b.room 
                                                                        ))
                 ) \
                     .penalize("same rooms together", HardSoftScore.ONE_SOFT)
    return a

def same_subjects_together(constraint_factory: ConstraintFactory):
    a = constraint_factory. \
            for_each_unique_pair(LectureClass, 
                    Joiners.equal(lambda l: l.division),
                    Joiners.equal(lambda l: l.timeslot.day_of_week),
                    Joiners.filtering(lambda a, b: diffisZero(a,b) and (a.subject!=b.subject 
                                                                        ))
                 ) \
                     .penalize("same subjects together", HardSoftScore.ONE_SOFT)
    return a

# After the break, classes should be different
def lab_and_room(constraint_factory: ConstraintFactory):
    a = constraint_factory. \
        for_each(LectureClass). \
            join(LectureClass, 
                    Joiners.equal(lambda l: l.division),
                    Joiners.equal(lambda l: l.timeslot.day_of_week),
                    Joiners.filtering(lambda a, b: classAfterBreak(a,b) and (a.room.name.split(" ")[0]!=b.room.name.split(" ")[0]))
                 ) \
                     .reward("classes after break are different", HardSoftScore.ofSoft(2))
    return a

# A ConstraintCollecter.func takes a function and returns a collector

    
def teachers_prefer_less_lectures(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass). \
        group_by(lambda lecture: (lecture.teacher, lecture.timeslot.day_of_week), ConstraintCollectors.count()). \
            filter(lambda lecture, cnt: cnt<4). \
                reward("less lectures are preferred by teachers", HardSoftScore.ofSoft(1))
    return a

# Lab subjects should be taught in a Lab and Room subjects should be taught in a room
def lecture_lab_room_conflict(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        filter(lambda l1: (l1.room.name.startswith("Lab") and (l1.subject not in lab_lectures)) or
                      (l1.room.name.startswith("Room") and (l1.subject not in room_lectures))).\
                penalize("lab lab room room", HardSoftScore.ONE_HARD)
    
    return a

def remove_overlapping_lectures(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each_unique_pair(LectureClass,
                    Joiners.equal(lambda l1: l1.teacher),
                    Joiners.equal(lambda l1: l1.subject),
                    Joiners.equal(lambda l1: l1.division),
                    Joiners.equal(lambda l1: l1.room),
                    Joiners.equal(lambda l1: l1.timeslot)
                    ).filter(lambda l1, l2: l1.id!=l2.id).penalize("overlapping", HardSoftScore.ofHard(2))
    return a

def cant_have_more_than_2_lectures(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.timeslot.day_of_week, l1.subject, l1.division), ConstraintCollectors.count()).\
            filter(lambda key,cnt: cnt>2).\
                penalize("cant have more than two lectures", HardSoftScore.ONE_HARD)
    return a

def same_labs_throughout(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.room, l1.division), ConstraintCollectors.count()).\
            filter(lambda key,cnt: key[0].name.startswith("Lab")).\
                group_by(lambda key,cnt: key[1], ConstraintCollectors.count_bi()).\
                    filter(lambda x,cnt: cnt>1).\
                        penalize("labs of divisions should remain same", HardSoftScore.ONE_HARD)
    return a

@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        room_conflict(constraint_factory),
        class_conflict(constraint_factory),
        teacher_conflict(constraint_factory),
        four_lectures_per_day(constraint_factory),
        same_rooms_together(constraint_factory),
        same_subjects_together(constraint_factory),
        lab_and_room(constraint_factory),
        teachers_prefer_less_lectures(constraint_factory),
        lecture_lab_room_conflict(constraint_factory),
        remove_overlapping_lectures(constraint_factory),
        cant_have_more_than_2_lectures(constraint_factory),
        same_labs_throughout(constraint_factory),
    ]
    