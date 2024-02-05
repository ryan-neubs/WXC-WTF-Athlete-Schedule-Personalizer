
class AthleteSchedule():

    def __init__(self, data):

        self.name = str(data[0].split(", ")[1]) + " " + str(data[0].split(", ")[0]) 
        self.mileage = data[2:9]
        self.fms = data[1]
        self.notes = data[-1]
        self.data = data
        self.tue_workout = None
        self.fri_workout = None

    def __call__(self):
        return self.mileage

    def get_name(self):
        return self.name
    
    def get_fms(self):
        return self.fms
    
    def get_notes(self):
        return self.notes
    
    def get_days_mileage(self, day):
        return self.mileage[day]