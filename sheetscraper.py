import os
import pandas as pd

os.chdir('./MileageSheets')

mileage = pd.read_excel('1-22-2024-Mileage.xlsx')

class AthleteSchedule():

    dow_index = {'MON':3, 'TUE':4, 'WED':5, 'THU':6, 'FRI':7, 'SAT':8, 'SUN':9}

    def __init__(self, data):

        self.name = data[0]
        self.mileage = data[3:9]
        self.fms = data[1]
        self.notes = data[-1]
        self.data = data

    def get_name(self):
        return self.name
    
    def get_fms(self):
        return self.fms
    
    def get_notes(self):
        return self.notes
    
    def get_days_mileage(self, day):
        return self.mileage[self.dow_index[day]]

athletes = []
for row in mileage.values.tolist():
    if "double core" in row[0] or "/" in row[0]:
        continue
    athletes.append(AthleteSchedule(row))

for item in athletes:
    print(item.get_name(), item.get_fms())