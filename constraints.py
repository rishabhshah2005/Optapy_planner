# <add python path if required>
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


def generate_subject_room(room: str):
    lst= []
    with open("input/subjects.txt", "r") as f:
        lines = f.readlines()
    
    for sub in lines:
        sub = sub.strip().split(" ")
        if sub[1]==room:
            lst.append(sub[0])
    
    return lst

lab_lectures = generate_subject_room("Lab")
room_lectures = generate_subject_room("Room")

def diffisZero(lesson1: Lecture, lesson2: Lecture):
    between = datetime.combine(today, lesson1.timeslot.end_time) - datetime.combine(today, lesson2.timeslot.start_time)
    between2 = datetime.combine(today, lesson2.timeslot.end_time) - datetime.combine(today, lesson1.timeslot.start_time)
    
    return (timedelta(minutes=0) == between) or (timedelta(minutes=0) == between2)

# Rooms should not be same
def room_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    a = constraint_factory. \
        for_each_unique_pair(LectureClass,
                        Joiners.equal(lambda l1: l1.room),
                        Joiners.equal(lambda l1: l1.timeslot),
                             ) \
                 .penalize("room conflict", HardSoftScore.ofHard(1))
    return a

def teacher_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    a = constraint_factory. \
        for_each_unique_pair(LectureClass,
                Joiners.equal(lambda l1: l1.teacher),
                Joiners.equal(lambda l1: l1.timeslot),
                )\
                .penalize("teacher conflict", HardSoftScore.ofHard(1))
    return a

# Division conflict
def class_conflict(constraint_factory: ConstraintFactory):
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    a = constraint_factory. \
        for_each_unique_pair(LectureClass, 
                             Joiners.equal(lambda l1: l1.division),
                             Joiners.equal(lambda l1: l1.timeslot)
                             )\
                 .penalize("class conflict", HardSoftScore.ofHard(1))
    return a

def subject_conflict(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        filter(lambda l1: l1.subject != l1.teacher.subject).\
            penalize("Teachers should be assigned there resp subjects", HardSoftScore.ofHard(1))
            
    return a

# Each day should have 4 lectures for each division
def four_lectures_per_day(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(Lecture)
                              .group_by(lambda lecture: (lecture.timeslot.day_of_week, lecture.division),  # group into lectures on the same day
                                        ConstraintCollectors.count())  # count lectures in the group
                              .filter(lambda day_of_week, count: count < 4)
                              .penalize("four lectures per day", HardSoftScore.ONE_HARD)
    )
    
# Lab subjects should be taught in a Lab and Room subjects should be taught in a room
def lecture_lab_room_conflict(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        filter(lambda l1: (l1.room.name.startswith("Lab") and (l1.subject not in lab_lectures)) or
                      (l1.room.name.startswith("Room") and (l1.subject not in room_lectures))).\
                penalize("lab lab room room", HardSoftScore.ofHard(2))
    return a

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

def remove_overlapping_lectures(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each_unique_pair(LectureClass,
                    Joiners.equal(lambda l1: l1.teacher),
                    Joiners.equal(lambda l1: l1.division),
                    Joiners.equal(lambda l1: l1.room),
                    Joiners.equal(lambda l1: l1.timeslot)
                    ).filter(lambda l1, l2: l1.id!=l2.id).penalize("overlapping", HardSoftScore.ofHard(1))
    return a

def cant_have_more_than_2_lectures(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.timeslot.day_of_week, l1.subject, l1.division), ConstraintCollectors.count()).\
            filter(lambda key,cnt: cnt>2).\
                penalize("cant have more than two lectures", HardSoftScore.ofHard(1))
    return a

def same_labs_throughout(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.room, l1.division), ConstraintCollectors.count()).\
            filter(lambda key,cnt: key[0].name.startswith("Lab")).\
                group_by(lambda key,cnt: key[1], ConstraintCollectors.count_bi()).\
                    filter(lambda x,cnt: cnt>1).\
                        penalize("labs of divisions should remain same", HardSoftScore.ONE_HARD)
    return a

def teachers_constant_division(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.teacher, l1.division)).\
            group_by(lambda l1: l1[0], ConstraintCollectors.count()).\
                filter(lambda grp, cnt: cnt>3).\
                    penalize("Teachers cant have more than 3 divisions", HardSoftScore.ONE_HARD)
    return a

def students_constant_teachers(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.division, l1.teacher)).\
            group_by(lambda l1: l1[0] ,ConstraintCollectors.count()).\
                filter(lambda grp, cnt: cnt>4).\
                    penalize("students should have the same teachers", HardSoftScore.ofHard(2))
    return a

def only_two_labs_per_day(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.timeslot.day_of_week, l1.division, l1.room.name.startswith("Lab")), ConstraintCollectors.count()).\
                filter(lambda grp, cnt: grp[2] and cnt>2).\
                    penalize("Cant have more than 2 labs per day", HardSoftScore.ONE_HARD)

    return a

def only_two_rooms_per_day(constraint_factory: ConstraintFactory):
    a = constraint_factory.for_each(LectureClass).\
        group_by(lambda l1: (l1.timeslot.day_of_week, l1.division, l1.room.name.startswith("Room")), ConstraintCollectors.count()).\
                filter(lambda grp, cnt: grp[2] and cnt>2).\
                    penalize("Cant have more than 2 rooms per day", HardSoftScore.ofHard(2))

    return a


@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        room_conflict(constraint_factory),# Hard
        class_conflict(constraint_factory), # Hard
        teacher_conflict(constraint_factory), # Hard
        subject_conflict(constraint_factory), # Hard
        four_lectures_per_day(constraint_factory), # Hard
        same_rooms_together(constraint_factory),
        same_subjects_together(constraint_factory),
        lecture_lab_room_conflict(constraint_factory), # Hard
        remove_overlapping_lectures(constraint_factory), # Hard
        cant_have_more_than_2_lectures(constraint_factory),
        same_labs_throughout(constraint_factory),
        teachers_constant_division(constraint_factory), 
        students_constant_teachers(constraint_factory),
        only_two_labs_per_day(constraint_factory),
        only_two_rooms_per_day(constraint_factory),
    ]
    