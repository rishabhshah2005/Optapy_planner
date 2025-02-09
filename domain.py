#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe
from optapy import planning_entity, planning_variable
from optapy import problem_fact, planning_id

from optapy import planning_solution, planning_entity_collection_property,problem_fact_collection_property, \
                value_range_provider, planning_score
from optapy.score import HardSoftScore
from datetime import time


# @problem_fact
# class Division:
#     def __init__(self, id, div):
#         self.div=div
#         self.id=id
        
#     @planning_id
#     def get_id(self):
#         return self.id
    
#     def __str__(self):
#         return f"Division(id={self.id}, div={self.div})"
        
    

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
                f"room_name={self.name})"
        )
 
@planning_entity
class Lecture:
    def __init__(self, id, teacher, subject,division,room=None, timeslot=None):
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
        
    @planning_variable(Room, ['roomRange'])
    def get_room(self):
        return self.room
    
    def set_room(self, new_room):
        self.room = new_room
        
        
        
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
    def __init__(self, timeslot_list, lecture_list,room_list, score=None):
        self.timeslot_list = timeslot_list
        self.lecture_list = lecture_list
        self.room_list = room_list
        self.score = score
        
    @problem_fact_collection_property(Timeslot)
    @value_range_provider("timeslotRange")
    def get_timeslot_list(self):
        return self.timeslot_list
    
    @problem_fact_collection_property(Room)
    @value_range_provider("roomRange")
    def get_room_list(self):
        return self.room_list
    
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
    
    division_list = [
        "A1",
        "A2",
        "A3",
    ]
    
    room_list = [
        Room(1,"Room 1"),
        Room(2,"Room 2"),
        # Room(3,"Room 3"),
        Room(4,"Lab 1"),
        Room(5,"Lab 2"),
        # Room(6,"Lab 3"),
        # Room(7,"Room 4"),
        # Room(8,"Lab 4"),
    ]
    # LECTURE(self, id, teacher, subject,division,room=None, timeslot=None)
    lecture_list = [
        Lecture(1, "DPB", "FSD", "A1"),
        Lecture(2, "MVP", "Python", "A1"),
        Lecture(3, "PKS", "PS", "A1"),
        Lecture(4, "UMS", "DE", "A1"),
        Lecture(5, "DPB", "FSD", "A1"),
        Lecture(6, "MVP", "Python", "A1"),
        Lecture(7, "PKS", "PS", "A1"),
        Lecture(8, "UMS", "DE", "A1"),
        Lecture(9, "DPB", "FSD", "A1"),
        Lecture(10, "MVP", "Python", "A1"),
        Lecture(11, "PKS", "PS", "A1"),
        Lecture(12, "UMS", "DE", "A1"),
        Lecture(13, "DPB", "FSD", "A1"),
        Lecture(14, "MVP", "Python", "A1"),
        Lecture(15, "PKS", "PS", "A1"),
        Lecture(16, "UMS", "DE", "A1"),
        Lecture(17, "DPB", "FSD", "A1"),
        Lecture(18, "MVP", "Python", "A1"),
        Lecture(19, "PKS", "PS", "A1"),
        Lecture(20, "UMS", "DE", "A1"),
        Lecture(21, "DPB", "FSD", "A1"),
        Lecture(22, "MVP", "Python", "A1"),
        Lecture(23, "PKS", "PS", "A1"),
        Lecture(24, "UMS", "DE", "A1"),
        
        Lecture(25, "DPB", "FSD", "A2"),
        Lecture(26, "MVP", "Python", "A2"),
        Lecture(27, "PKS", "PS", "A2"),
        Lecture(28, "UMS", "DE", "A2"),
        Lecture(29, "DPB", "FSD", "A2"),
        Lecture(30, "MVP", "Python", "A2"),
        Lecture(31, "PKS", "PS", "A2"),
        Lecture(32, "UMS", "DE", "A2"),
        Lecture(33, "DPB", "FSD", "A2"),
        Lecture(34, "MVP", "Python", "A2"),
        Lecture(35, "PKS", "PS", "A2"),
        Lecture(36, "UMS", "DE", "A2"),
        Lecture(37, "DPB", "FSD", "A2"),
        Lecture(38, "MVP", "Python", "A2"),
        Lecture(39, "PKS", "PS", "A2"),
        Lecture(40, "UMS", "DE", "A2"),
        Lecture(41, "DPB", "FSD", "A2"),
        Lecture(42, "MVP", "Python", "A2"),
        Lecture(43, "PKS", "PS", "A2"),
        Lecture(44, "UMS", "DE", "A2"),
        Lecture(45, "DPB", "FSD", "A2"),
        Lecture(46, "MVP", "Python", "A2"),
        Lecture(47, "PKS", "PS", "A2"),
        Lecture(48, "UMS", "DE", "A2"),
        
        Lecture(49, "DPB", "FSD", "A3"),
        Lecture(50, "MVP", "Python", "A3"),
        Lecture(51, "PKS", "PS", "A3"),
        Lecture(52, "UMS", "DE", "A3"),
        Lecture(53, "DPB", "FSD", "A3"),
        Lecture(54, "MVP", "Python", "A3"),
        Lecture(55, "PKS", "PS", "A3"),
        Lecture(56, "UMS", "DE", "A3"),
        Lecture(57, "DPB", "FSD", "A3"),
        Lecture(58, "MVP", "Python", "A3"),
        Lecture(59, "PKS", "PS", "A3"),
        Lecture(60, "UMS", "DE", "A3"),
        Lecture(61, "DPB", "FSD", "A3"),
        Lecture(62, "MVP", "Python", "A3"),
        Lecture(63, "PKS", "PS", "A3"),
        Lecture(64, "UMS", "DE", "A3"),
        Lecture(65, "DPB", "FSD", "A3"),
        Lecture(66, "MVP", "Python", "A3"),
        Lecture(67, "PKS", "PS", "A3"),
        Lecture(68, "UMS", "DE", "A3"),
        Lecture(69, "DPB", "FSD", "A3"),
        Lecture(70, "MVP", "Python", "A3"),
        Lecture(71, "PKS", "PS", "A3"),
        Lecture(72, "UMS", "DE", "A3"),
        
]

    
    
    lesson = lecture_list[0]
    lesson.set_timeslot(timeslot_list[0])
    lesson.set_room(room_list[0])

    return TimeTable(timeslot_list, lecture_list, room_list)