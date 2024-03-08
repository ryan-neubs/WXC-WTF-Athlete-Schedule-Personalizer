import os
import pandas as pd


def scrape_mileage_sheet(sheet, week):
    os.chdir("./MileageSheets/")
    mileagesheets = pd.ExcelFile(sheet)
    mileage = pd.read_excel(mileagesheets, week)
    os.chdir("..")
    return mileage.values.tolist()

def scrape_workout_sheet(sheet, week):
    subtables = []
    os.chdir("./static/WorkoutSheets/")
    workoutsheets = pd.ExcelFile(sheet)
    workout = pd.read_excel(workoutsheets, week)
    workout = workout.astype(str)
    os.chdir("../..")
    data = workout.values.tolist()
    colnames = [row for row in workout]
    colname = colnames[0]
    for row in data:
        if row[0] == 'nan':
            row[0] = colname
    data.insert(0, colnames)
    data[0][0] = colname
    for row in data:
        if (row[0] == colname and row[12] == 'nan') or row[-2] == 'nan':
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

def get_workouts(sheet):
    workouts = {}
    wo = pd.read_excel(sheet)
    rows = wo.values.tolist()
    for row in rows:
        if type(row[-1]) == str:
            workouts[row[-1].split(':')[0]] = row[-1].split(':')[1]
    return workouts


    