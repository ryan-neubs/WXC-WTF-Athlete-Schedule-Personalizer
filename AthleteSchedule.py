import pandas
from workout import Workout
class AthleteSchedule():

    CORE = {
        0:['Crunches', 'Mountain Climbers', 'V-Hold', 'Push Ups', 'Side Crunch Right', 'Side Crunch Left', 'Plank', 'Plank ins and outs', 'Side Plank Right', 'Side Plank Left', 'Supermans', 'V Crunches'],
        1:['Woodchop Left', 'Woodchop Right', 'Woodchop Center', 'Push Ups', 'Pocket Pickers', 'Plank', 'Plank with leg lifts', 'Push-Ups', 'Lowers and Outs', 'Crossovers', 'Dips-right', 'Dips-left', 'Bicycle'],
        2:['Side Crunch Left', 'Side Crunch Right', 'Plank Opp Elbow Opp Knee','Windmill Push Ups', 'Reverse Crunch', 'Superman Opposite Arm Opposite Leg', 'Dive Bombers', 'Side to Side Crunch', 'Flutter Kick', 'Side to Side Plank', 'Push Ups', 'Lemon Squeezers', 'Crunches'],
        3:['Windmill Push Ups', 'Back Bridge with Leg Lifts', 'Plank', 'Side Plank', 'Star Plank', 'Pump Crunch', 'Reverse Crunch'],
        4:['Need to find in season friday core list'],
        5:['Superman', 'V-Ups', 'Plank with toe taps', 'Bicycle Crunch', 'Side Plank + Leg Crunch', 'Pocket Pickers', 'Push Ups', 'Burner (Plank, Push-up, Plank Up Down)'],
        6:['Superman', 'V-Ups', 'Plank with toe taps', 'Bicycle Crunch', 'Side Plank + Leg Crunch', 'Pocket Pickers', 'Push Ups', 'Burner (Plank, Push-up, Plank Up Down)']
        }

    def __init__(self, data):

        self.name = str(data[0].split(", ")[1]) + " " + str(data[0].split(", ")[0]) 
        self.mileage = data[2:9]
        self.fms = data[1]
        if pandas.isna(self.fms):
            self.fms = 'None'
        self.notes = data[-1]
        if pandas.isna(self.notes):
            self.notes = 'None'
        self.data = data
        if self.mileage[1] == 'WO':
            self.tue_workout = True
        if self.mileage[4] == 'WO':
            self.fri_workout = True
        self.total_miles = data[9]

    def __call__(self):
        return self.mileage
    
    def get_total_miles(self):
        return self.total_miles

    def get_name(self):
        return self.name
    
    def get_fms(self):
        return self.fms
    
    def get_notes(self):
        return self.notes
    
    def get_days_mileage(self, day):
        return self.mileage[day]

    def get_core(self, day):
        return self.CORE[day]