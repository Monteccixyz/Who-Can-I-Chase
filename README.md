# Who Can I Chase

A machine learning project to predict which birds can be observed based on weather conditions, location, and time.

## Project Goal

Given a location, date, and weather conditions, predict which bird species are likely to be observable. This helps birders plan their outings by knowing what to expect.

## Current Scope

- **Region**: Andalucía, Spain
- **Weather Data**: 2025 (1 year)
- **Bird Data**: eBird observations from 2020-2025

We initially planned to cover all of Spain with 5 years of weather data, but pivoted to Andalucía only due to API rate limits on Open-Meteo's historical weather endpoint.

## Data Sources

- **eBird**: Bird observation data from the Cornell Lab of Ornithology
- **Open-Meteo**: Historical weather data (temperature, humidity, precipitation, wind, cloud cover)

## Project Structure

```
who-can-i-chase/
├── data/
│   ├── raw/              # Original downloaded files (eBird, weather)
│   └── processed/        # Cleaned, joined datasets
├── notebooks/            # Exploration and prototyping
├── src/
│   ├── data/             # Data loading and processing scripts
│   │   ├── fetch_weather.py           # Weather API functions
│   │   ├── fetch_weather_unattended.py # Batch weather fetcher
│   │   └── prepare_coords.py          # Coordinate extraction
│   ├── features/         # Feature engineering
│   └── models/           # Model training and prediction
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the Weather Fetcher

1. First, prepare the coordinates file for Andalucía:

```bash
cd src/data
python prepare_coords.py
```

This will create `data/processed/unique_coords.csv` with unique coordinate pairs (rounded to 0.1 degree precision) from Andalucía observations.

2. Then run the weather fetcher:

```bash
python fetch_weather_unattended.py
```

The fetcher will:
- Process coordinates in batches of 10
- Sleep 120 seconds between batches to respect API rate limits
- Save progress incrementally to `data/processed/weather_andalucia_2025.csv`
- Track progress in `data/processed/fetch_progress.txt` so it can resume if interrupted

## Dependencies

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **requests** - HTTP requests for weather API
- **python-dotenv** - Environment variable management
- **jupyter** - Interactive notebooks
- **scikit-learn** - Machine learning
- **matplotlib** - Plotting and visualization
- **seaborn** - Statistical data visualization
