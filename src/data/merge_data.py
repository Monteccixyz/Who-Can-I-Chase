import pandas as pd

import os

# Get the directory where this script lives
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data')

weather_df = pd.read_csv(os.path.join(DATA_DIR, 'processed', 'weather_andalucia_2025.csv'))

bird_df = pd.read_csv(os.path.join(DATA_DIR, 'raw', 'ebird_spain_2020-2025.txt'),
    delimiter='\t',
    usecols=['COMMON NAME', 'SCIENTIFIC NAME', 'OBSERVATION DATE', 'LATITUDE', 'LONGITUDE', 'STATE']
)

# Filter to Andalucía
bird_df = bird_df[bird_df['STATE'] == 'Andalucía']

# Round coordinates to match weather data
bird_df['lat_rounded'] = bird_df['LATITUDE'].round(1)
bird_df['lon_rounded'] = bird_df['LONGITUDE'].round(1)

# Rename date column to match
bird_df['date'] = bird_df['OBSERVATION DATE']

# Now merge
merged = pd.merge(bird_df, weather_df,
                  left_on=['date', 'lat_rounded', 'lon_rounded'],
                  right_on=['date', 'latitude', 'longitude'])

print(len(merged))

