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
A. Run one by one the files in the [src](./src/) folder:
```
python3 src/get_data.py
python3 src/get_train_test.py
python3 src/model_train_predict.py
```
B. Use the bash script:
```
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```
> Note that some plot will be appearing during the execution, you can look at them to see how the model performs.
> The results of the predictions will be stored on the [predictions](./predictions/) folder and the models on the [models](./models/) folder.

You can as well run it online on a prepared [Google Colab](https://colab.research.google.com/drive/1ROKeqyYTzW2muFEA1-dAsgBHwFxoVSh8?usp=sharing).
