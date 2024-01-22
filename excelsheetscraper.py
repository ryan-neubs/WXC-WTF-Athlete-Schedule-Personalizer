import os
import pandas as pd


def scrape_milage_sheet(sheet):
    os.chrdir("./MileageSheets")
    mileage = pd.read_excel(sheet)
    return mileage.values.tolist()