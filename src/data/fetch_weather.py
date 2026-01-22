import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

url = "https://archive-api.open-meteo.com/v1/archive"

def fetch_weather(start_date, end_date, lat: list, lon: list):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "wind_speed_100m", "wind_gusts_10m"]
    }
    responses = openmeteo.weather_api(url, params=params)

    dataframes = []

    for response in responses:
    # Process first location. Add a for-loop for multiple locations or weather models

        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        for index, name in enumerate(params["hourly"]):
            hourly_data[name] = hourly.Variables(index).ValuesAsNumpy()

        hourly_data["latitude"] = response.Latitude()
        hourly_data["longitude"] = response.Longitude()

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        dataframes.append(hourly_dataframe)

    return pd.concat(dataframes)

# if __name__ == "__main__":
#     start = "2025-10-02"
#     end = "2025-12-02"
#     lat = [37.2, 36.8, 36.8, 37.2]
#     lon = [-2.5, -2.3, -2.2, -1.8]
#     df = fetch_weather(start, end, lat, lon)
#     print(df)

