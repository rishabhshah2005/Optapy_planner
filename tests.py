# <add python path if required>
from domain import Lecture, Timeslot, TimeTable, Room, Teacher
from constraints import *
from datetime import time
from optapy.test import ConstraintVerifier, constraint_verifier_build

cv: ConstraintVerifier = constraint_verifier_build(define_constraints, TimeTable, Lecture)

DIV1 = "A1"
DIV2 = "A2"
DIV3 = "A3"
DIV4 = "A4"
DIV5 = "A5"

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

S1 = Teacher(1, "UMS", "DE")
S2 = Teacher(2, "MVP", "Python")
S3 = Teacher(3, "DPB", "FSD")
S4 = Teacher(4, "PKS", "PS")
S5 = Teacher(5, "PHA", "FSD")
S6 = Teacher(6, "AAP", "Python")
S7 = Teacher(7, "SAS", "PS")
S8 = Teacher(8, "UMM", "DE")

# LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
def test_room_conflict():
    first_lesson = Lecture(1, DIV1, "DE", S1, R1, T1)
    conflicting_lesson = Lecture(2, DIV2, "DE", S1, R1, T1)
    nonconflicting_lesson = Lecture(3, DIV2, "DE", S1, R1, T2)
    cv.verify_that(room_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_class_conflict():
    first_lesson = Lecture(1, DIV1, "DE", S1, R1, T1)
    conflicting_lesson = Lecture(2, DIV1, "DE", S2, R2, T1)
    nonconflicting_lesson = Lecture(3, DIV1, "DE", S2, R1, T2)
    cv.verify_that(class_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_teacher_conflict():
    first_lesson = Lecture(1, DIV1, "DE", S1, R1, T1)
    conflicting_lesson = Lecture(2, DIV2, "DE", S1, R1, T1)
    nonconflicting_lesson = Lecture(3, DIV2, "DE", S1, R1, T2)
    cv.verify_that(teacher_conflict).given(first_lesson, conflicting_lesson, nonconflicting_lesson). \
        penalizes_by(1)
        
def test_same_classes_conflict():
    valid_lectures = [   
            Lecture(1 ,DIV1, "DE", S1, R1, T1),
            Lecture(2 ,DIV1, "DE", S1, R1, T2),
            Lecture(3 ,DIV1, "DE", S2, R1, T3),
            Lecture(4 ,DIV1, "DE", S2, R1, T4),
        ]

    invalid_lectures = [   
            Lecture(1, DIV1, "DE", S1,R1, T1),
            Lecture(2, DIV1, "DE", S1,R2, T2),
            Lecture(3, DIV1, "DE", S1,R2, T3),
            Lecture(4, DIV1, "DE", S2,L1, T4),
        ]
    
    # Verify that the correct cases are penalized
    cv.verify_that(same_rooms_together) \
        .given(*valid_lectures) \
        .penalizes(0)  # No penalty for valid case

    cv.verify_that(same_rooms_together) \
        .given(*invalid_lectures) \
        .penalizes(2)  # Penalized for missing a lecture
                
def test_four_lectures_per_day():
    valid_lectures = [   
        Lecture(1, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV1, "DE", S1, R1, T2),
        Lecture(3, DIV1, "DE", S1, R1, T3),
        Lecture(4, DIV1, "DE", S1, R1, T4),
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
        
def test_lecture_lab_room_conflict():
    valid_lectures = [
        Lecture(1, DIV1, "Python", S2, L1, T1),
        Lecture(2, DIV2, "FSD", S3, L2, T2),
        Lecture(3, DIV1, "DE", S1, R1, T3),
    ]
    invalid_lectures2 = [
        Lecture(6, DIV1, "DE", S1, L1, T1),
        Lecture(2, DIV2, "DE", S1, L2, T2),
    ]
    invalid_lectures = [
        Lecture(7, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S4, R2, T2),
        Lecture(3, DIV1, "FSD", S2, R1, T3),
        Lecture(4, DIV1, "Python", S3, R2, T4),
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
    first_lesson = Lecture(1, DIV1, "DE", S1, R1, T1)
    conflicting_lesson = Lecture(2, DIV1, "DE", S1, R1, T1)
    nonconflicting_lesson = Lecture(3, DIV1, "DE", S1, R1, T2)
    cv.verify_that(remove_overlapping_lectures).given(first_lesson, nonconflicting_lesson, conflicting_lesson). \
        penalizes(1)

def test_cant_have_more_than_2_lectures():
    valid_lectures = [
        Lecture(1, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S1, R2, T2),
        Lecture(3, DIV1, "FSD", S2, R1, T3),
        Lecture(4, DIV1, "FSD", S2, R1, T4),
    ]
    invalid_lectures2 = [
        Lecture(1, DIV2, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S1, R2, T2),
        Lecture(3, DIV2, "DE", S1, R2, T3),
        Lecture(4, DIV2, "DE", S1, R2, T4),
    ]
    valid_lectures2 = [
        Lecture(1, DIV1, "FSD", S1, R1, T1),
        Lecture(2, DIV2, "DE", S2, R2, T2),
        Lecture(3, DIV1, "DE", S3, R1, T3),
        Lecture(4, DIV1, "DE", S3, R1, T4),
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
        Lecture(1, DIV2, "DE", S2, L1, T1),
        Lecture(2, DIV2, "DE", S2, L1, T2),
        Lecture(3, DIV1, "DE", S1, L1, T3),
        Lecture(4, DIV1, "DE", S1, L1, T4),
        Lecture(4, DIV1, "DE", S1, L1, T4),
        Lecture(4, DIV1, "DE", S1, L1, T4),
    ]
    invalid_lectures2 = [
        Lecture(1, DIV2, "DE", S2, L1, T1),
        Lecture(2, DIV2, "DE", S2, L2, T2),
        Lecture(3, DIV1, "DE", S2, L1, T3),
        Lecture(4, DIV1, "DE", S2, L2, T4),
        Lecture(4, DIV1, "DE", S2, L3, T4),
    ]
    valid_lectures2 = [
        Lecture(1, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S2, R2, T2),
        Lecture(3, DIV1, "DE", S3, L1, T3),
        Lecture(4, DIV1, "DE", S3, L1, T4),
        Lecture(4, DIV1, "DE", S4, L1, T4),
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
        
def test_teachers_constant_division():
    valid_lectures = [
        Lecture(1, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S1, R2, T2),
        Lecture(3, DIV3, "DE", S1, L1, T3),
        Lecture(4, DIV1, "DE", S3, L1, T4),
        Lecture(5, DIV1, "DE", S4, L1, T4),
    ]
    valid_lectures2 = [
        Lecture(1, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S1, R2, T2),
        Lecture(3, DIV3, "DE", S2, L1, T3),
        Lecture(4, DIV1, "DE", S3, L1, T4),
        Lecture(5, DIV1, "DE", S4, L1, T4),
    ]
    invalid_lectures = [
        Lecture(1, DIV1, "DE", S1, R1, T1),
        Lecture(2, DIV2, "DE", S1, R2, T2),
        Lecture(3, DIV3, "DE", S1, L1, T3),
        Lecture(4, DIV4, "DE", S1, L1, T4),
        Lecture(5, DIV1, "DE", S4, L1, T5),
    ]
    
    cv.verify_that(teachers_constant_division).\
        given(*valid_lectures).\
            penalizes(0)
    cv.verify_that(teachers_constant_division).\
        given(*valid_lectures2).\
            penalizes(0)
    cv.verify_that(teachers_constant_division).\
        given(*invalid_lectures).\
            penalizes(1)

def test_subject_conflict():
    invalid_lectures = [
        Lecture(1, DIV1,'DE', S1, R1, T1),
        Lecture(1, DIV1,'DE', S2, R1, T1),
        Lecture(1, DIV1,'DE', S3, R1, T1),
        Lecture(1, DIV1,'DE', S4, R1, T1),
    ]
    
    valid_lectures = [
        Lecture(1, DIV1,'DE', S1, R1, T1),
        Lecture(1, DIV1,'Python', S2, R1, T1),
        Lecture(1, DIV1,'FSD', S3, R1, T1),
        Lecture(1, DIV1,'PS', S4, R1, T1),
    ]
    
    cv.verify_that(subject_conflict).\
        given(*invalid_lectures).\
            penalizes(3)
    cv.verify_that(subject_conflict).\
        given(*valid_lectures).\
            penalizes(0)

def test_students_constant_teachers():
    invalid_lectures = [
        Lecture(1, DIV1,'DE', S1, R1, T1),
        Lecture(1, DIV1,'DE', S2, R1, T1),
        Lecture(1, DIV1,'DE', S3, R1, T1),
        Lecture(1, DIV1,'DE', S4, R1, T1),
        Lecture(1, DIV1,'DE', S5, R1, T1),
    ]
    
    valid_lectures = [
        Lecture(1, DIV1,'DE', S1, R1, T1),
        Lecture(1, DIV1,'Python', S2, R1, T1),
        Lecture(1, DIV1,'FSD', S3, R1, T1),
        Lecture(1, DIV1,'PS', S4, R1, T1),
        Lecture(1, DIV2,'DE', S1, R1, T1),
    ]
    
    cv.verify_that(students_constant_teachers).\
        given(*invalid_lectures).\
            penalizes(1)
    cv.verify_that(students_constant_teachers).\
        given(*valid_lectures).\
            penalizes(0)

def test_only_two_labs_per_day():
    invalid_lectures = [
        Lecture(1, DIV1,'FSD', S2, L1, T1),
        Lecture(2, DIV1,'FSD', S2, L1, T2),
        Lecture(3, DIV1,'Python', S3, L2, T3),
        Lecture(4, DIV1,'Python', S3, L2, T4),
    ]
    valid_lectures = [
        Lecture(1, DIV1,'FSD', S2, L1, T1),
        Lecture(2, DIV1,'FSD', S2, L1, T2),
        Lecture(3, DIV1,'DE', S1, R2, T3),
        Lecture(4, DIV1,'DE', S1, R2, T4),
    ]
    
    
    cv.verify_that(only_two_labs_per_day).\
        given(*invalid_lectures).\
            penalizes(1)
    cv.verify_that(only_two_labs_per_day).\
        given(*valid_lectures).\
            penalizes(0)
