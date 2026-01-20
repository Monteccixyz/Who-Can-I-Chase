# Who Can I Chase

A ML project for observation recommendations based on eBird and weather data.

## Project Structure

```
who-can-i-chase/
├── data/
│   ├── raw/           # Original downloaded files (eBird, weather)
│   └── processed/     # Cleaned, joined datasets
├── notebooks/         # Exploration and prototyping
├── src/
│   ├── data/          # Data loading and processing scripts
│   ├── features/      # Feature engineering
│   └── models/        # Model training and prediction
├── requirements.txt
└── README.md
```

## Dependencies

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **requests** - HTTP requests for eBird and weather APIs
- **python-dotenv** - Environment variable management
- **jupyter** - Interactive notebooks
- **scikit-learn** - Machine learning
- **matplotlib** - Plotting and visualization
- **seaborn** - Statistical data visualization

## Setup

```bash
pip install -r requirements.txt
```
