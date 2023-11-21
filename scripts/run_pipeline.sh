#!/bin/bash

pip install -r requirements.txt
python3 src/get_data.py #--update_load --update_gen
python3 src/get_train_test.py
python3 src/model_train_predict.py