from math import isnan
import pandas as pd
from excelsheetscraper import scrape_workout_sheet

class Workout:

    def __init__(self, data):
        # These variables are all time estimates to calculate paces
        PERCENT = 0.58
        self.fivek = data[1]
        self.mile = data[2]
        self.threek = data[3]
        self.R = data[5]
        self.VO2 = data[6]
        self.I = data[7]
        self.tenk = data[8]
        self.CV = data[9]
        self.thresh = data[10]
        self.threshlow = data[11]
        # End of calculation constants
        def get_splits(data):
            splits = []
            for split in data[11:]:
                if split == 'nan':
                    break
                splits.append(split)
            return splits
        
        self.splits = get_splits(data)
        self.athlete = data[0]
        self.group = data[-2]
        # self.workout = workouts[data[-2]] Inconsistency in excel form, need to think of different solution
    
    def get_group(self):
        return self.group
    
    def get_athlete(self):
        return self.athlete
    
    def get_splits(self):
        return self.splits
    
    