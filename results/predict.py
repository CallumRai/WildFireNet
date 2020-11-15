import keras
import os
import requests
import json
import pandas as pd
import numpy
import warnings
warnings.filterwarnings('ignore')

def zip_to_coord(zip, df):
    # converts a zip code to approx geocode
    row = df.loc[zip, :]
    lat = row['latitude']
    lon = row['longitude']

    lat = round(lat, 0)
    lon = round(lon, 0)

    return lat, lon


def predict(lat, lon, day, month, year, df, model):
    # forms a prediction based on coord
    index = str(((lat, lon), (day, month)))

    row = df.loc[index, :]
    row['year'] = year

    col_no = len(df.columns)
    arr = row.values.reshape(1, col_no)
    return model.predict(arr)


def zip_predict(zip, day, month, year, df_coord, df_predict, model):
    # forms a prediction based on zip
    lat, lon = zip_to_coord(zip, df_coord)
    prediction = predict(lat, lon, day, month, year, df_predict, model)
    return prediction


def input_predict(df, model):
    valid = False

    while not valid:
        try:
            lat = float(input("Latitude in USA: "))
            lon = float(input("Longitude in USA: "))
            day = int(input("Day: "))
            month = int(input("Month: "))
            year = int(input("Year: "))

            lat = round(lat, 0)
            lon = round(lon, 0)

            predictions = predict(lat, lon, day, month, year, df, model)

            valid = True
        except Exception:
            print("\nInvalid entry, (is your geocode in the USA and date valid)")
            valid = False

    fire_7 = round(predictions[0][0] * 100, 1)
    fire_30 = round(predictions[0][1] * 100, 1)
    print("\n% chance of fire in 7 days: " + str(fire_7) + "%")
    print("% chance of fire in 30 days: " + str(fire_30) + "%")


def input_zip_predict(df_coord, df_predict, model):
    valid = False

    while not valid:
        try:
            zip = int(input("Zip: "))
            day = int(input("Day: "))
            month = int(input("Month: "))
            year = int(input("Year: "))

            predictions = zip_predict(zip, day, month, year, df_coord, df_predict, model)

            valid = True
        except Exception:
            print("\nInvalid entry, (is your geocode in the USA and date valid)")
            valid = False

    fire_7 = round(predictions[0][0] * 100, 1)
    fire_30 = round(predictions[0][1] * 100, 1)
    print("\n% chance of fire in 7 days: " + str(fire_7) + "%")
    print("% chance of fire in 30 days: " + str(fire_30) + "%")


def main():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    model = keras.models.load_model(data_path + "\\wildfire_net_v1.h5")
    df_predict = pd.read_csv(data_path + "\\prediction.csv", index_col=0)
    df_coord = pd.read_csv(data_path + "\\coord\\Geocodes_USA_with_Counties.csv", index_col=0)

if __name__ == "__main__":
    main()
