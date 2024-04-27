# APD-Detection-Yolov8

## About
This is a simple AI Application to detect Personel Protective Equipment (PPE) or <i> Alat Pelindung Diri </i>. I fine-tuned Yolov8n model with dataset to make model better detect PPE. I use streamlit framework as a dashboard application. This application can detect PPE through image or video even a YouTube video. You can use your own file or the sample data given.

## Dataset
I use dataset from kaggle "[Construction Site Safety Image Dataset Roboflow](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow)". I use this dataset because this dataset have been annotated and have enough label to detect PPE. 

## Preview Dashboard
![[Preview Demo Video Detection]](./img/preview.png)

## How to run application

- clone this repo by typing `git clone`
- Open the terminal and go to dashboard directory
- Type `python -m venv .venv` and hit enter
- Type `.venv/Scripts/activate` and hit enter for `Windows`
- Type `source .venv/bin/activate` and hit enter for `MacOS`
- Then type `pip install -r requirements.txt`
- Now open the API by typing `streamlit run main.py`
- Wait until it finish. it will run on `http://localhost:8501`
