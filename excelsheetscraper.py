import os
import pandas as pd


def scrape_mileage_sheet(week):
    os.chdir("./Sheets/")
    mileagesheets = pd.ExcelFile("Mileage.xlsx")
    mileage = pd.read_excel(mileagesheets, week)
    os.chdir("..")
    return mileage.values.tolist()

def scrape_workout_sheet(week):
    subtables = []
    os.chdir("./Sheets/")
    workoutsheets = pd.ExcelFile("Workouts.xlsx")
    workout = pd.read_excel(workoutsheets, week)
    workout = workout.astype(str)
    os.chdir("..")
    data = workout.values.tolist()
    colnames = [row for row in workout]
    colname = colnames[0]
    for row in data:
        if row[0] == 'nan':
            row[0] = colname
    data.insert(0, colnames)
    data[0][0] = colname
    for row in data:
        if (row[0] == colname and row[12] == 'nan'):
            data.remove(row)
    labellocs = []
    rowloc = 0
    for row in data:
        if row[0] == colname and (row[1] != 'nan' or row[12] != 'nan'):
            labellocs.append(rowloc)
        rowloc += 1
    for index in range(len(labellocs)):
        if index + 1 == len(labellocs):
            subtables.append(data[labellocs[index]:])
        else:
            subtables.append(data[labellocs[index]:labellocs[index+1]])
    return subtables

def get_workouts(week): # Issue - Workouts for women are being overwritten due to the keys being the same name
    workoutsW = {}
    workoutsM = {}
    os.chdir("./Sheets/")
    wosheet = pd.ExcelFile("Workouts.xlsx")
    wo = pd.read_excel(wosheet, week)
    os.chdir("..")
    # The first A group workout is put on the column label row causing it to be cut off. 
    # The next two lines fix that
    hiddenlabel, hiddendata = [row for row in wo.astype(str)][-1].split(':')
    workoutsW[hiddenlabel] = hiddendata
    rows = wo.values.tolist()
    for row in rows:
        if type(row[-1]) == str:
            if not row[-1].split(':')[0] in workoutsW:
                workoutsW[row[-1].split(':')[0]] = row[-1].split(':')[1]
            else:
                workoutsM[row[-1].split(':')[0]] = row[-1].split(':')[1]
    return workoutsW, workoutsM

def get_roster_list():
    os.chdir("./Sheets/")
    rosters = pd.read_excel("Roster.xlsx")
    os.chdir("..")
    return rosters["Men"].tolist(), rosters["Women"].tolist()
    
    

    