import pandas as pd
from sqlite import Table


def convert(channel):
    selection = Table().select(channel)
# creating pandas dataframe from dictionary of data

    df_cars = pd.DataFrame(selection, columns=[
        'name_channel', 'date', 'number_users'])

# Exporting dataframe to Excel file
    df_cars.to_excel(f"xlsx/{channel}.xlsx", sheet_name='name')
