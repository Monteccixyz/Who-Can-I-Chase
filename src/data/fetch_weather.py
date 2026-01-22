import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in daily is important to assign them correctly below

url = "https://archive-api.open-meteo.com/v1/archive"

def fetch_weather(start_date, end_date, lat: list, lon: list):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_mean", "relative_humidity_2m_mean", "cloud_cover_mean", "precipitation_sum", "rain_sum", "wind_gusts_10m_mean", "wind_speed_10m_mean"]
    }
    responses = openmeteo.weather_api(url, params=params)

    dataframes = []

    for response in responses:
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}

        for index, name in enumerate(params["daily"]):
            daily_data[name] = daily.Variables(index).ValuesAsNumpy()

        daily_data["latitude"] = response.Latitude()
        daily_data["longitude"] = response.Longitude()

        daily_dataframe = pd.DataFrame(data=daily_data)
        dataframes.append(daily_dataframe)

    return pd.concat(dataframes)

if __name__ == "__main__":
    lat = [37.2, 36.8]
    lon = [-2.5, -2.3]
    df = fetch_weather("2020-01-01", "2020-01-10", lat, lon)
    print(df)
