#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from domain import Division, Lecture, Timeslot, TimeTable
from constraints import *
from datetime import time
from optapy.test import ConstraintVerifier, constraint_verifier_build

cv: ConstraintVerifier = constraint_verifier_build(define_constraints, TimeTable, Lecture)

DIV1 = Division(1, "A1")
DIV2 = Division(2, "A2")

T1 = Timeslot(1, "MONDAY", time(hour=8, minute=45), time(hour=9, minute=45))
T2 = Timeslot(2, "MONDAY", time(hour=9, minute=45), time(hour=10, minute=45))
T3 = Timeslot(3, "MONDAY", time(hour=11, minute=30), time(hour=12, minute=30))
T4 = Timeslot(4, "MONDAY", time(hour=12, minute=30), time(hour=13, minute=30))
T5 = Timeslot(5, "TUESDAY", time(hour=8, minute=45), time(hour=9, minute=45))


# LECTURE(self, id, room, teacher, subject, timeslot=None, division=None)
def test_room_conflict():
    first_lesson = Lecture(1, "Room1", "Teacher A", "DE", T1, DIV1)
    conflicting_lesson = Lecture(2, "Room1", "Teacher A", "DE", T1, DIV2)
    nonconflicting_lesson = Lecture(3, "Room1", "Teacher A", "DE", T2, DIV2)
    cv.verify_that(room_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_class_conflict():
    first_lesson = Lecture(1, "Room1", "Teacher A", "DE", T1, DIV1)
    conflicting_lesson = Lecture(2, "Room1", "Teacher A", "DE", T1, DIV1)
    nonconflicting_lesson = Lecture(3, "Room1", "Teacher A", "DE", T2, DIV2)
    cv.verify_that(class_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_teacher_conflict():
    first_lesson = Lecture(1, "Room1", "Teacher A", "DE", T1, DIV1)
    conflicting_lesson = Lecture(2, "Room1", "Teacher A", "DE", T1, DIV1)
    nonconflicting_lesson = Lecture(3, "Room1", "Teacher A", "DE", T2, DIV2)
    cv.verify_that(teacher_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_same_classes_conflict():
    first_lesson = Lecture(1, "Room1", "Teacher A", "DE", T1, DIV1)
    conflicting_lesson = Lecture(2, "Room1", "Teacher B", "PS", T2, DIV1)
    nonconflicting_lesson = Lecture(3, "Room1", "Teacher A", "DE", T2, DIV1)
    cv.verify_that(same_classes_together).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
# C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe -m pytest tests.py