# Who Can I Chase

A machine learning project to predict which birds might be observable based on weather conditions, location, and time of year in Andalucía, Spain.

## Project Goal

Given a location, date, and weather conditions, predict which bird species are likely to be observable. This could help birders plan their outings by knowing what to expect.

## Current Status

This is an early prototype. We have a working model that achieves ~84% recall on detecting bird presence, though precision is low (~15%). In practice, this means the model tends to over-predict (it will suggest birds that may not actually appear), but it catches most of the birds that do show up. There's plenty of room for improvement.

### What Works
- Data pipeline from eBird observations through weather data to training
- XGBoost binary classifier for presence/absence prediction
- Basic handling of the severe class imbalance (~22:1 negative to positive)

### Known Limitations
- Only covers Andalucía region (due to weather API rate limits)
- Only uses 2025 weather data
- Low precision means many false positives
- No hyperparameter tuning yet
- Model doesn't account for habitat type, elevation, or time of day
- The negative example assumption (species not recorded = not present) is imperfect

## Data Sources

- **eBird**: Bird observation data from the Cornell Lab of Ornithology (2020-2025)
- **Open-Meteo**: Historical weather data (temperature, humidity, precipitation, wind, cloud cover)

## Project Structure

```
who-can-i-chase/
├── data/
│   ├── raw/                    # Original downloaded files (eBird, weather)
│   └── processed/              # Cleaned, joined datasets
│       ├── unique_coords.csv       # Coordinate pairs for weather fetching
│       ├── weather_andalucia_2025.csv  # Daily weather data
│       └── training_data.csv       # Final ML-ready dataset (~10.6M rows)
├── notebooks/
│   ├── explore_ebird.ipynb     # Initial data exploration
│   ├── merging.ipynb           # Joining bird + weather data
│   ├── prepare_training.ipynb  # Generate negatives, add features
│   └── train_model.ipynb       # Model training and evaluation
├── models/
│   ├── bird_model.pkl          # Trained XGBoost model
│   └── label_encoder.pkl       # Species label encoder
├── src/
│   └── data/
│       ├── fetch_weather.py           # Weather API functions
│       ├── fetch_weather_unattended.py # Batch weather fetcher
│       └── prepare_coords.py          # Coordinate extraction
├── requirements.txt
└── README.md
```

## Data Pipeline

1. **eBird data** - Download observation data for the region
2. **Weather fetching** - Get historical weather for each unique coordinate
3. **Merging** - Join bird observations with weather conditions
4. **Training prep** - Generate negative examples, add temporal features
5. **Training** - Train XGBoost classifier

### Training Data Details

- **488 species** tracked in the dataset
- **~21,700 unique checklists** (location + date combinations)
- **~10.6 million rows** after generating negative examples
- **~4.3% positive class** (bird was seen), **~95.7% negative** (not seen)

### Features Used

| Feature | Description |
|---------|-------------|
| `lat_rounded`, `lon_rounded` | Location (0.1 degree precision) |
| `temperature_2m_mean` | Daily mean temperature |
| `relative_humidity_2m_mean` | Daily mean humidity |
| `cloud_cover_mean` | Daily mean cloud cover |
| `precipitation_sum` | Daily precipitation total |
| `rain_sum` | Daily rain total |
| `wind_gusts_10m_mean` | Daily mean wind gusts |
| `wind_speed_10m_mean` | Daily mean wind speed |
| `day_of_year` | Day of year (1-365) for seasonality |
| `month` | Month (1-12) |
| `species_encoded` | Encoded species identifier |

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Fetching Weather Data

1. Prepare the coordinates file:
```bash
cd src/data
python prepare_coords.py
```

2. Run the weather fetcher (this takes a while due to API rate limits):
```bash
python fetch_weather_unattended.py
```

### Training the Model

Run through the notebooks in order:
1. `explore_ebird.ipynb` - Understand the raw data
2. `merging.ipynb` - Join bird and weather data
3. `prepare_training.ipynb` - Create training dataset
4. `train_model.ipynb` - Train and evaluate the model

### Making Predictions

```python
import joblib
import pandas as pd

model = joblib.load('models/bird_model.pkl')
le = joblib.load('models/label_encoder.pkl')

# Create input for all species at a given location/weather
conditions = pd.DataFrame({
    'lat_rounded': [37.2] * 488,
    'lon_rounded': [-2.5] * 488,
    'temperature_2m_mean': [12.0] * 488,
    # ... other weather features ...
    'day_of_year': [15] * 488,
    'month': [1] * 488,
    'species_encoded': range(488)
})

probs = model.predict_proba(conditions)[:, 1]
conditions['species'] = le.inverse_transform(conditions['species_encoded'])
conditions['probability'] = probs

# Get top predicted birds
top_birds = conditions[['species', 'probability']].sort_values('probability', ascending=False)
```

## Dependencies

- pandas - Data manipulation
- numpy - Numerical computing
- requests - Weather API calls
- xgboost - Gradient boosting classifier
- scikit-learn - ML utilities
- joblib - Model serialization
- jupyter - Notebooks
- matplotlib, seaborn - Visualization

## Future Ideas

- Add more features (habitat, elevation, time of day)
- Try different models or ensemble approaches
- Tune hyperparameters
- Expand to other regions (if API limits allow)
- Build a simple web interface for predictions
- Improve negative example generation (maybe sample proportionally to species rarity)
