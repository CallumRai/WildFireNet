import pandas as pd
import os
from datetime import date, timedelta
import requests
import json
import time


def coord_samples(df):
    # gets all lat, lon samples in USA

    df = df.round({'latitude': 0, 'longitude': 0})
    df = df.drop_duplicates(subset=['latitude', 'longitude'])
    lat_long = df.loc[:, ['latitude', 'longitude']].values.tolist()
    lat_long_tuple = [tuple(i) for i in lat_long]

    return lat_long_tuple


def init_df(lat_lon, start_year, end_year):
    # creates df for very coord, date combination

    sdate = date(start_year, 1, 1)
    edate = date(end_year, 1, 1)
    delta = edate - sdate

    days = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        days.append(day)

    coord_day = tuple([(coord, day) for coord in lat_lon for day in days])
    lat = []
    lon = []
    year = []
    month = []
    day = []
    date_col = []
    for i in coord_day:
        lat.append(i[0][0])
        lon.append(i[0][1])
        year.append(i[1].year)
        month.append(i[1].month)
        day.append(i[1].day)
        date_col.append(i[1])

    data = {'lat': lat, 'lon': lon, 'year': year, 'month': month, 'day': day, 'date': date_col}
    coord_day = [str(i) for i in coord_day]
    df = pd.DataFrame(data=data, index=coord_day)

    return df


def init_fire(df):
    # initialises dataframe containing data on location and date of fires

    df['date'] = pd.to_datetime(df['acq_date'], infer_datetime_format=True)

    df = df.round({'latitude': 0, 'longitude': 0})
    df = df.drop_duplicates(subset=['latitude', 'date', 'longitude'])
    df['coord_day'] = df.apply(lambda row: str(((row['latitude'], row['longitude']), row['date'].date())), axis=1)
    df.set_index('coord_day', inplace=True)

    df['fire'] = 1

    return df


def index_fire(df, days):
    # creates df with whether there is a fire in x days time

    date_col = 'date_' + str(days)
    df[date_col] = df['date'] - timedelta(days=days)

    coord_day_col = 'coord_day_' + str(days)
    df[coord_day_col] = df.apply(lambda row: str(((row['latitude'], row['longitude']), row[date_col].date()))
                                 , axis=1)
    df.set_index(coord_day_col, inplace=True, drop=True)
    df = df['fire']
    df = df.rename('fire_' + str(days))

    return df.to_frame()


def combine(dfs, subset):
    # combines two dataframes

    for i in range(len(dfs)):
        dfs[i] = dfs[i][~dfs[i].index.duplicated(keep='first')]

    df = pd.concat(dfs, axis=1)

    df.dropna(subset=subset, inplace=True)
    df.fillna(0, inplace=True)

    return df


def api_data(coords, syear, eyear):
    # collects weather data for a set of coordinates

    # api collects data for 45 days, creates list of days in intervals that form a year
    first_date = date(2016, 1, 1)
    next_date = first_date + timedelta(days=44)
    date45 = [first_date]
    year = 2016
    while year == 2016:
        date45.append(next_date + timedelta(days=1))
        next_date += timedelta(days=45)
        year = next_date.year

    day_month = [(i.day, i.month) for i in date45]
    dfs = []
    for coord in coords:
        for k in range(len(day_month)):

            # for last part of year, only want 6 days
            d = day_month[k]
            if k == len(day_month) - 1:
                no = 6
            else:
                no = 45

            lat = coord[0]
            lon = coord[1]
            day = d[0]
            month = d[1]

            url = "https://api.weather.com/v3/wx/almanac/daily/45day?geocode=" + str(lat) + "%2C" + str(lon) + \
                  "&units=m&startDay=" + str(day) + "&startMonth=" + str(month) + \
                  "&format=json&apiKey=5424e9662cbf4bc3a4e9662cbf4bc3fe"
            try:
                data_url = requests.get(url)
            except Exception:
                print("API Failed")
                continue

            if data_url.status_code != 200:
                continue

            data_json = data_url.json()

            # duplicates api data for each year we are training on
            lat_lon = (lat, lon)
            for year in range(syear, eyear + 1):
                year_json = dict(data_json)

                coord_date = []
                for i in range(45):
                    datei = year_json['almanacRecordDate'][i]
                    month = int(datei[:2])
                    day = int(datei[2:])
                    try:
                        coord_date.append(str((lat_lon, date(year, month, day))))
                    except ValueError:
                        coord_date.append(str((lat_lon, date(year, 2, 28))))

                year_json['coord_date'] = coord_date
                df = pd.DataFrame(year_json).iloc[:no]
                dfs.append(df)

    all_data = pd.concat(dfs)
    all_data = all_data[['precipitationAverage', 'temperatureAverageMax', 'temperatureAverageMin', 'temperatureMean',
                         'temperatureRecordMax', 'temperatureRecordMin', 'coord_date']]
    all_data.set_index("coord_date", inplace=True)
    return all_data


def main():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    # initiliase df w/ coord, dates in usa
    coord_df = pd.read_csv(data_path + "\\coord\\Geocodes_USA_with_Counties.csv")
    coords = coord_samples(coord_df)
    coord_df = init_df(coords, 2016, 2020)

    # initiliase fire df
    fire_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')) + "\\fire\\"
    fire_dfs = [pd.read_csv(fire_path + f) for f in os.listdir(fire_path)]
    fire_df = pd.concat(fire_dfs)
    fire_df = init_fire(fire_df)

    # get fire in 7/30 days time and combine w coord, data df
    fire_7 = index_fire(fire_df, 7)
    fire_30 = index_fire(fire_df, 30)
    df = combine([coord_df, fire_7, fire_30], ['lat'])

    # combine api data to df
    api_df = api_data(coords, 2016, 2019)
    df = combine([df, api_df], ['temperatureMean'])

    df.to_csv(data_path + "\\dataset_clean.csv")


if __name__ == "__main__":
    main()
