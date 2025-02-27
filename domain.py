#! C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from optapy import planning_entity, planning_variable
from optapy import problem_fact, planning_id

from optapy import planning_solution, planning_entity_collection_property,problem_fact_collection_property, \
                value_range_provider, planning_score
from optapy.score import HardSoftScore
from datetime import time


@problem_fact
class Timeslot:
    def __init__(self, id, day_of_week, start_time, end_time):
        self.id = id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return (
                f"Timeslot("
                f"id={self.id}, "
                f"day_of_week='{self.day_of_week}', "
                f"start_time='{self.start_time}', "
                f"end_time='{self.end_time}')"
        )

@problem_fact
class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    @planning_id
    def get_id(self):
        return self.id
    def __str__(self):
        return (
                f"Room("
                f"id={self.id}, "
                f"name='{self.name}')"
        )
 
@problem_fact
class Teacher:
    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject = subject
    
    @planning_id
    def get_id(self):
        return self.id
    def __str__(self):
        return (
                f"Teacher("
                f"id={self.id}, "
                f"name='{self.name}',"
                f"subject='{self.subject}')"
        )

@planning_entity
class Lecture:
    def __init__(self, id, division, subject ,teacher=None, room=None, timeslot=None):
        self.id = id
        self.room = room
        self.teacher = teacher
        self.timeslot = timeslot
        self.division = division
        self.subject = subject
        
    @planning_id
    def get_id(self):
        return self.id
    
    @planning_variable(Timeslot, ['timeslotRange'])
    def get_timeslot(self):
        return self.timeslot
    
    def set_timeslot(self, new_timeslot):
        self.timeslot = new_timeslot
        
    @planning_variable(Room, ['roomRange'])
    def get_room(self):
        return self.room
    
    def set_room(self, new_room):
        self.room = new_room
    
    @planning_variable(Teacher, ['teacherRange'])    
    def get_teacher(self):
        return self.teacher
    
    def set_teacher(self, new_teacher):
        self.teacher = new_teacher
        
    def __str__(self):
        return (
            f"Lecture("
            f"id={self.id}, "
            f"timeslot={self.timeslot}, "
            f"room={self.room}, "
            f"teacher={self.teacher}, "
            f"division='{self.division}', "
            f"subject='{self.subject}', "
            f")"
        )

def format_list(a_list):
    return ',\n'.join(map(str, a_list))

@planning_solution
class TimeTable:
    def __init__(self, timeslot_list, lecture_list,room_list,teacher_list, score=None):
        self.timeslot_list = timeslot_list
        self.lecture_list = lecture_list
        self.room_list = room_list
        self.teacher_list = teacher_list
        self.score = score
        
    @problem_fact_collection_property(Timeslot)
    @value_range_provider("timeslotRange")
    def get_timeslot_list(self):
        return self.timeslot_list
    
    @problem_fact_collection_property(Room)
    @value_range_provider("roomRange")
    def get_room_list(self):
        return self.room_list
    
    @problem_fact_collection_property(Teacher)
    @value_range_provider("teacherRange")
    def get_teacher_list(self):
        return self.teacher_list
    
    @planning_entity_collection_property(Lecture)
    def get_lecture_list(self):
        return self.lecture_list
    
    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score
    
    def __str__(self):
        return (
            f"TimeTable("
            f"timeslot_list={format_list(self.timeslot_list)},\n"
            f"lecture_list={format_list(self.lecture_list)},\n"
            f"score={str(self.score.toString()) if self.score is not None else 'None'}"
            f")"  
        )      

def create_lectures(divs):
    lst = []
    cnt=0
    subs = ["DE", "PS", "FSD", "Python"]
    for i in range(1, divs+1):
         for sub in subs:
             for j in range(6):
                 lst.append(Lecture(cnt, "A"+str(i), sub))
                 cnt+=1
    return lst
             

def generate_problem():
    
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THRUSDAY", "FRIDAY", "SATURDAY"]           
            
    timeslot_list = [
        Timeslot(1, "MONDAY", time(hour=8, minute=45), time(hour=9, minute=45)),
        Timeslot(2, "MONDAY", time(hour=9, minute=45), time(hour=10, minute=45)),
        Timeslot(3, "MONDAY", time(hour=11, minute=30), time(hour=12, minute=30)),
        Timeslot(4, "MONDAY", time(hour=12, minute=30), time(hour=13, minute=30)),
        Timeslot(5, "TUESDAY", time(hour=8, minute=45), time(hour=9, minute=45)),
        Timeslot(6, "TUESDAY", time(hour=9, minute=45), time(hour=10, minute=45)),
        Timeslot(7, "TUESDAY", time(hour=11, minute=30), time(hour=12, minute=30)),
        Timeslot(8, "TUESDAY", time(hour=12, minute=30), time(hour=13, minute=30)),
        Timeslot(9, "WEDNESDAY", time(hour=8, minute=45), time(hour=9, minute=45)),
        Timeslot(10, "WEDNESDAY", time(hour=9, minute=45), time(hour=10, minute=45)),
        Timeslot(11, "WEDNESDAY", time(hour=11, minute=30), time(hour=12, minute=30)),
        Timeslot(12, "WEDNESDAY", time(hour=12, minute=30), time(hour=13, minute=30)),
        Timeslot(13, "THURSDAY", time(hour=8, minute=45), time(hour=9, minute=45)),
        Timeslot(14, "THURSDAY", time(hour=9, minute=45), time(hour=10, minute=45)),
        Timeslot(15, "THURSDAY", time(hour=11, minute=30), time(hour=12, minute=30)),
        Timeslot(16, "THURSDAY", time(hour=12, minute=30), time(hour=13, minute=30)),
        Timeslot(17, "FRIDAY", time(hour=8, minute=45), time(hour=9, minute=45)),
        Timeslot(18, "FRIDAY", time(hour=9, minute=45), time(hour=10, minute=45)),
        Timeslot(19, "FRIDAY", time(hour=11, minute=30), time(hour=12, minute=30)),
        Timeslot(20, "FRIDAY", time(hour=12, minute=30), time(hour=13, minute=30)),
        Timeslot(21, "SATURDAY", time(hour=8, minute=45), time(hour=9, minute=45)),
        Timeslot(22, "SATURDAY", time(hour=9, minute=45), time(hour=10, minute=45)),
        Timeslot(23, "SATURDAY", time(hour=11, minute=30), time(hour=12, minute=30)),
        Timeslot(24, "SATURDAY", time(hour=12, minute=30), time(hour=13, minute=30)),
    ]
    
    # Teacher(self, id, name, subject)
    teacher_list = [
        Teacher(1, "UMS", "DE"),
        Teacher(2, "MVP", "Python"),
        Teacher(3, "DPB", "FSD"),
        Teacher(4, "PKS", "PS"),
        Teacher(5, "PHA", "FSD"),
        Teacher(6, "AAP", "Python"),
        Teacher(7, "SAS", "PS"),
        Teacher(8, "UMM", "DE"),
        Teacher(9, "ZVB", "DE"),
        Teacher(10, "KMS", "Python"),
        Teacher(11, "DVP", "Python"),
        Teacher(12, "PBZ", "FSD"),
        Teacher(13, "SAS", "FSD"),
        Teacher(14, "MGV", "PS"),
    ]
    
    room_list = [
        Room(1,"Room 1"),
        Room(2,"Room 2"),
        Room(3,"Room 3"),
        Room(4,"Lab 1"),
        Room(5,"Lab 2"),
        Room(6,"Lab 3"),
        Room(7,"Room 4"),
        Room(8,"Lab 4"),
        Room(9,"Lab 5"),
        Room(10,"Room 5"),
    ]
    # LECTURE(id, division, subject ,teacher=None, room=None, timeslot=None)
    lecture_list = create_lectures(9)
    
    lesson: Lecture = lecture_list[0]
    lesson.set_timeslot(timeslot_list[0])
    lesson.set_room(room_list[0])
    lesson.set_teacher(teacher_list[0])

    return TimeTable(timeslot_list, lecture_list, room_list, teacher_list)