#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from domain import Lecture, Timeslot, TimeTable, Room
from constraints import *
from datetime import time
from optapy.test import ConstraintVerifier, constraint_verifier_build

cv: ConstraintVerifier = constraint_verifier_build(define_constraints, TimeTable, Lecture)

DIV1 = "A1"
DIV2 = "A2"

T1 = Timeslot(1, "MONDAY", time(hour=8, minute=45), time(hour=9, minute=45))
T2 = Timeslot(3, "MONDAY", time(hour=9, minute=45), time(hour=10, minute=45))
T3 = Timeslot(2, "MONDAY", time(hour=11, minute=30), time(hour=12, minute=30))
T4 = Timeslot(4, "MONDAY", time(hour=12, minute=30), time(hour=13, minute=30))
T5 = Timeslot(5, "TUESDAY", time(hour=8, minute=45), time(hour=9, minute=45))

R1 = Room(1, "Room 1")
R2 = Room(2, "Room 2")
L1 = Room(3, "Lab 1")
L2 = Room(4, "Lab 2")
L3 = Room(5, "Lab 3")


# LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
def test_room_conflict():
    first_lesson = Lecture(1,"Teacher A", "DE", DIV1, R1, T1)
    conflicting_lesson = Lecture(2,"Teacher A", "DE", DIV2, R1, T1)
    nonconflicting_lesson = Lecture(3,"Teacher A", "DE", DIV2, R1, T2)
    cv.verify_that(room_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_class_conflict():
    first_lesson = Lecture(1,"Teacher A", "DE", DIV1, R1, T1)
    conflicting_lesson = Lecture(2,"Teacher B", "PS", DIV1, R2, T1)
    nonconflicting_lesson = Lecture(3,"Teacher B", "PS", DIV1, R1, T2)
    cv.verify_that(class_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_teacher_conflict():
    first_lesson = Lecture(1,"Teacher A", "DE", DIV1, R1, T1)
    conflicting_lesson = Lecture(2,"Teacher A", "DE", DIV2, R1, T1)
    nonconflicting_lesson = Lecture(3,"Teacher A", "DE", DIV2, R1, T2)
    cv.verify_that(teacher_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_same_classes_conflict():
    valid_lectures = [   
            Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
            Lecture(2,"Teacher A", "DE", DIV1, R1, T2),
            Lecture(3,"Teacher A", "PS", DIV1, R1, T3),
            Lecture(4,"Teacher A", "PS", DIV1, R1, T4),
        ]

    invalid_lectures = [   
            Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
            Lecture(2,"Teacher A", "DE", DIV1, R2, T2),
            Lecture(3,"Teacher A", "DE", DIV1, R2, T3),
            Lecture(4,"Teacher A", "PS", DIV1, L1, T4),
        ]
    
    # Verify that the correct cases are penalized
    cv.verify_that(same_rooms_together) \
        .given(*valid_lectures) \
        .penalizes(0)  # No penalty for valid case

    cv.verify_that(same_rooms_together) \
        .given(*invalid_lectures) \
        .penalizes(2)  # Penalized for missing a lecture
        
        
def test_lab_and_room():
    first_lesson = Lecture(1,"Teacher A", "DE", DIV1, R1, T2)
    conflicting_lesson = Lecture(2,"Teacher A", "DE", DIV1, R1, T3)
    nonconflicting_lesson = Lecture(3,"Teacher A", "DE", DIV1, L1, T3)
    cv.verify_that(lab_and_room).given(first_lesson, nonconflicting_lesson, conflicting_lesson). \
        rewards(1)
        
def test_four_lectures_per_day():
    valid_lectures = [   
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "DE", DIV1, R1, T2),
        Lecture(3,"Teacher A", "DE", DIV1, R1, T3),
        Lecture(4,"Teacher A", "DE", DIV1, R1, T4),
    ]

    # Invalid case: 3 lectures (should be penalized)
    invalid_lectures = valid_lectures[:-1]  # Remove 1 lecture
    
    # Verify that the correct cases are penalized
    cv.verify_that(four_lectures_per_day) \
        .given(*valid_lectures) \
        .penalizes(0)  # No penalty for valid case

    cv.verify_that(four_lectures_per_day) \
        .given(*invalid_lectures) \
        .penalizes(1)  # Penalized for missing a lecture
        
def test_teachers_prefer_less_lectures():
    valid_lectures = [
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "DE", DIV2, R2, T2),
        Lecture(3,"Teacher A", "DE", DIV1, R1, T3),
    ]
    valid_lectures2 = [
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "DE", DIV2, R2, T2),
    ]
    invalid_lectures = [
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "DE", DIV2, R2, T2),
        Lecture(3,"Teacher A", "DE", DIV1, R1, T3),
        Lecture(4,"Teacher A", "DE", DIV1, R1, T4),
    ]

 
    # Verify that the correct cases are rewarded
    cv.verify_that(teachers_prefer_less_lectures) \
        .given(*valid_lectures) \
        .rewards(1)  
    cv.verify_that(teachers_prefer_less_lectures) \
        .given(*valid_lectures2) \
        .rewards(1)  

    # No rewards for 4 lectures
    # cv.verify_that(teachers_prefer_less_lectures) \
    #     .given(*invalid_lectures) \
    #     .rewards(0)  

def test_lecture_lab_room_conflict():
    valid_lectures = [
        Lecture(1,"Teacher A", "FSD", DIV1, L1, T1),
        Lecture(2,"Teacher A", "FSD", DIV2, L2, T2),
        Lecture(3,"Teacher A", "DE", DIV1, R1, T3),
    ]
    invalid_lectures2 = [
        Lecture(6,"Teacher A", "DE", DIV1, L1, T1),
        Lecture(2,"Teacher A", "PS", DIV2, L2, T2),
    ]
    invalid_lectures = [
        Lecture(7,"Teacher A", "FSD", DIV1, R1, T1),
        Lecture(2,"Teacher A", "Python", DIV2, R2, T2),
        Lecture(3,"Teacher A", "DE", DIV1, R1, T3),
        Lecture(4,"Teacher A", "PS", DIV1, R2, T4),
    ]
    
    cv.verify_that(lecture_lab_room_conflict).\
        given(*valid_lectures).\
            penalizes(0)
    cv.verify_that(lecture_lab_room_conflict).\
        given(*invalid_lectures).\
            penalizes(2)
    cv.verify_that(lecture_lab_room_conflict).\
        given(*invalid_lectures2).\
            penalizes(2)

def test_remove_overlapping_lectures():
    first_lesson = Lecture(1,"Teacher A", "DE", DIV1, R1, T1)
    conflicting_lesson = Lecture(2,"Teacher A", "DE", DIV1, R1, T1)
    nonconflicting_lesson = Lecture(3,"Teacher A", "DE", DIV1, R1, T2)
    cv.verify_that(remove_overlapping_lectures).given(first_lesson, nonconflicting_lesson, conflicting_lesson). \
        penalizes(1)

def test_cant_have_more_than_2_lectures():
    valid_lectures = [
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "DE", DIV2, R2, T2),
        Lecture(3,"Teacher A", "PS", DIV1, R1, T3),
        Lecture(4,"Teacher A", "PS", DIV1, R1, T4),
    ]
    invalid_lectures2 = [
        Lecture(1,"Teacher A", "DE", DIV2, R1, T1),
        Lecture(2,"Teacher A", "DE", DIV2, R2, T2),
        Lecture(3,"Teacher A", "DE", DIV2, R2, T3),
        Lecture(4,"Teacher A", "DE", DIV2, R2, T4),
    ]
    valid_lectures2 = [
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "PS", DIV2, R2, T2),
        Lecture(3,"Teacher A", "FSD", DIV1, R1, T3),
        Lecture(4,"Teacher A", "FSD", DIV1, R1, T4),
    ]

 
    # Verify that the correct cases are rewarded
    cv.verify_that(cant_have_more_than_2_lectures) \
        .given(*valid_lectures) \
        .penalizes(0)  
    cv.verify_that(cant_have_more_than_2_lectures) \
        .given(*valid_lectures2) \
        .penalizes(0) 
    cv.verify_that(cant_have_more_than_2_lectures) \
        .given(*invalid_lectures2) \
        .penalizes(1)
        
def test_same_labs_throughout():
    valid_lectures = [
        Lecture(1,"Teacher A", "Python", DIV2, L1, T1),
        Lecture(2,"Teacher A", "Python", DIV2, L1, T2),
        Lecture(3,"Teacher A", "FSD", DIV1, L1, T3),
        Lecture(4,"Teacher A", "FSD", DIV1, L1, T4),
        Lecture(4,"Teacher A", "FSD", DIV1, L1, T4),
        Lecture(4,"Teacher A", "FSD", DIV1, L1, T4),
    ]
    invalid_lectures2 = [
        Lecture(1,"Teacher A", "FSD", DIV2, L1, T1),
        Lecture(2,"Teacher A", "FSD", DIV2, L2, T2),
        Lecture(3,"Teacher A", "FSD", DIV1, L1, T3),
        Lecture(4,"Teacher A", "FSD", DIV1, L2, T4),
        Lecture(4,"Teacher A", "FSD", DIV1, L3, T4),
    ]
    valid_lectures2 = [
        Lecture(1,"Teacher A", "DE", DIV1, R1, T1),
        Lecture(2,"Teacher A", "PS", DIV2, R2, T2),
        Lecture(3,"Teacher A", "FSD", DIV1, L1, T3),
        Lecture(4,"Teacher A", "FSD", DIV1, L1, T4),
        Lecture(4,"Teacher A", "Python", DIV1, L1, T4),
    ]

 
    # Verify that the correct cases are rewarded
    cv.verify_that(same_labs_throughout) \
        .given(*valid_lectures) \
        .penalizes(0)  
    cv.verify_that(same_labs_throughout) \
        .given(*valid_lectures2) \
        .penalizes(0) 
    cv.verify_that(same_labs_throughout) \
        .given(*invalid_lectures2) \
        .penalizes(2) 

# C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe -m pytest tests.py