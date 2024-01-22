import os
import pandas as pd


def scrape_milage_sheet(sheet):
    os.chrdir("./MileageSheets")
    mileage = pd.read_excel('1-22-2024-Mileage.xlsx')
    return mileage.values.tolist()