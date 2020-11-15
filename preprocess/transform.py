import pandas as pd
import os
from datetime import date, timedelta
import requests
import json
import time


def interaction(df, cols):
    # combines variables to consider there dependent effects

    col_name = ""
    for c in cols:
        col_name += "_" + c
    col_name = col_name[1:]

    df[col_name] = df[cols[0]]

    for i in range(1, len(cols)):
        df[col_name] = df[col_name] * df[cols[1]]

    return df


def ohe(df, col):
    # one hot encode
    df_ohe = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, df_ohe], axis=1)
    df = df.drop(columns=[col])
    return df


def normalise(df, col):
    # x[i] - mean(x) / std(x) to normalise [not used]

    df[col] = (df[col] - df[col].mean()) / df[col].std()
    df = df.rename({col: col + str("_norm")})
    return df

def clean_to_features(df):
    # remove redundant features
    df = df.drop(columns=['date'])

    # ohe month
    df = ohe(df, 'month')

    # create list of desired interactions
    interactions = [['lat', 'lon'], ['lat', 'precipitationAverage'], ['lat', 'temperatureMean'],
                    ['lon', 'precipitationAverage'], ['lon', 'temperatureMean']]
    for i in range(1, 13):
        month_col = 'month_' + str(float(i))

        lat_int = [month_col, 'lat']
        lon_int = [month_col, 'lon']

        interactions.append(lat_int)
        interactions.append(lon_int)

    for i in interactions:
        df = interaction(df, i)

    # reorganise columns
    cols = list(df.columns)
    cols.remove("fire_7")
    cols.remove("fire_30")

    df = df[cols + ["fire_7", "fire_30"]]
    return df

def main():
    df_clean = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
                     + "\\dataset.csv", index_col=0)

    df_features = clean_to_features(df_clean)

    df_features.to_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
              + "\\dataset_train.csv")


if __name__ == "__main__":
    main()
