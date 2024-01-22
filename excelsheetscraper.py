import os
import pandas as pd


def scrape_mileage_sheet(sheet):
    os.chdir("./MileageSheets/")
    mileage = pd.read_excel(sheet)
    return mileage.values.tolist()