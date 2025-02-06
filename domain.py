#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from optapy import planning_entity, planning_variable
from optapy import problem_fact, planning_id

from optapy import planning_solution, planning_entity_collection_property,problem_fact_collection_property, \
                value_range_provider, planning_score
from optapy.score import HardSoftScore
from datetime import time


@problem_fact
class Division:
    def __init__(self, id, div):
        self.div=div
        self.id=id
        
    @planning_id
    def get_id(self):
        return self.id
    
    def __str__(self):
        return f"Division(id={self.id}, div={self.div})"
        
    

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
                f"day_of_week={self.day_of_week}, "
                f"start_time={self.start_time}, "
                f"end_time={self.end_time})"
        )


@planning_entity
class Lecture:
    def __init__(self, id, room, teacher, subject, timeslot=None, division=None):
        self.id = id
        self.room = room
        self.teacher = teacher
        self.subject = subject
        self.timeslot = timeslot
        self.division = division
        
    @planning_id
    def get_id(self):
        return self.id
    
    @planning_variable(Timeslot, ['timeslotRange'])
    def get_timeslot(self):
        return self.timeslot
    
    def set_timeslot(self, new_timeslot):
        self.timeslot = new_timeslot
        
    
    @planning_variable(Division, ['divisionRange'])
    def get_division(self):
        return self.division
    
    def set_division(self, new_division):
        self.division = new_division
        
        
    def __str__(self):
        return (
            f"Lecture("
            f"id={self.id}, "
            f"timeslot={self.timeslot}, "
            f"room={self.room}, "
            f"teacher={self.teacher}, "
            f"subject={self.subject}, "
            f"divison={self.division}"
            f")"
        )

def format_list(a_list):
    return ',\n'.join(map(str, a_list))

@planning_solution
class TimeTable:
    def __init__(self, timeslot_list, division_list, lecture_list, score=None):
        self.timeslot_list = timeslot_list
        self.division_list = division_list
        self.lecture_list = lecture_list
        self.score = score
        
    @problem_fact_collection_property(Timeslot)
    @value_range_provider("timeslotRange")
    def get_timeslot_list(self):
        return self.timeslot_list
    
    @problem_fact_collection_property(Division)
    @value_range_provider("divisionRange")
    def get_division_list(self):
        return self.division_list
    
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
            f"division_list={format_list(self.division_list)},\n"
            f"lecture_list={format_list(self.lecture_list)},\n"
            f"score={str(self.score.toString()) if self.score is not None else 'None'}"
            f")"
        )      
    

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
    
    divsion_list = [
        Division(1, "A1"),
    ]
    # LECTURE(self, id, room, teacher, subject, timeslot=None, division=None)
    lecture_list = [
        Lecture(1, "Room 1", "Urmi Shah", "DE"),
        Lecture(2, "Room 1", "Prakruti Shah", "PS"),
        Lecture(8, "Lab 1", "Dhruvi Bhatt", "FSD"),
        Lecture(4, "Lab 1", "Dhruvi Bhatt", "FSD"),
        Lecture(3, "Lab 1", "Manish Patel", "Python"),
        Lecture(5, "Room 1", "Urmi Shah", "DE"),
        Lecture(6, "Room 1", "Prakruti Shah", "PS"),
        Lecture(7, "Lab 1", "Manish Patel", "Python"),
    ]
    
    
    lesson = lecture_list[0]
    lesson.set_timeslot(timeslot_list[0])
    lesson.set_division(divsion_list[0])

    return TimeTable(timeslot_list, divsion_list, lecture_list)