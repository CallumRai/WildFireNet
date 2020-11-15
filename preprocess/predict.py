import os
import pandas as pd
import transform
import keras
import numpy as np


def reindex(df):
    # remove year from index
    df['coord_date'] = df.apply(lambda row: str(((row['lat'], row['lon']), (int(row['day']), int(row['month'])))),
                                axis=1)
    df.set_index('coord_date', drop=True, inplace=True)
    return df


def main():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    df = pd.read_csv(data_path + "\\dataset_clean.csv", index_col=0)

    # only want data from one year (so we can vary year when predicting)
    df = df[df['year'] == 2019]

    # transforms into features we can predict upon
    df = reindex(df)
    df = transform.clean_to_features(df)
    df.drop(columns=['fire_7', 'fire_30'], inplace=True)

    df.to_csv(data_path + "\\prediction.csv")


if __name__ == "__main__":
    main()
