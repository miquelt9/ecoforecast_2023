# Ecoforecast Challenge 2023
EcoForecast: Revolutionizing Green Energy Surplus Prediction in Europe

### The problem

This is a Nuew challenge [link](https://nuwe.io/dev/competitions/schneider-electric-european-2023/ecoforecast-revolutionizing-green-energy-surplus-prediction-in-europe) the goal of which is to predict which country on a list will be the one with the most surplus of green energy.

Since we don't receive the data directly neither for doing the predictions, we retrieved it using ENTSOE API, and split it into the [test_data.csv](./data/test_data.csv) and [train_data.csv](./data/train_data.csv).

### Run the model yourself

- Depending on your PC you might need to do it in a virtual environment (I personally had to):
```
python -m venv path/to/venv
source path/to/venv/bin/activate
```
- Then install the requirements:
```
pip install -r requirements.txt
```
**Note**: that all the exections must be done from the main folder in order for them to work properly.
- After you can:
A. Run one by one the files in the [src](.src/) folder:
```

```
