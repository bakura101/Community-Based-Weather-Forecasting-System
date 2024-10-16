#Loading Modules Needed
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import pickle

#URL of the API made with Flask (Commented for now)
# API = "http://127.0.0.1:5000"

MODEL_PATH = './model/weather_model.pkl'
SCALER_PATH = './model/scaler.pkl'
IMG_SIDEBAR_PATH = "./assets/img.jpg"

#Function to load the Model and the Scaler
def load_pkl(fname):
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    return obj

try:
    model = load_pkl(MODEL_PATH)
    scaler = load_pkl(SCALER_PATH)
except FileNotFoundError as e:
    st.error(f"Error loading model or scaler: {e}")

#Function to load the dataset
def get_clean_data():
    return pd.read_csv("./dataset/weather_dataset.csv")

#Sidebar of the Streamlit App
def add_sidebar():
    st.sidebar.header("Community Based Weather Forecasting System")
    image = np.array(Image.open(IMG_SIDEBAR_PATH))
    st.sidebar.image(image)
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

    st.sidebar.subheader('Select the Weather Parameters ✅:')
  
    data = get_clean_data()
  
    slider_labels = [
        ("Precipitation", "precipitation"),
        ("Max Temperature", "temp_max"),
        ("Min Temperature", "temp_min"),
        ("Wind", "wind"),
    ]

    input_dict = {}

    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label,
            min_value=float(data[key].min()),
            max_value=float(data[key].max()),
            value=float(data[key].mean())
        )
    
    return input_dict

def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data.drop(['weather'], axis=1)
  
    scaled_dict = {}
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
  
    return scaled_dict

#Receiving Prediction Results from the model
def add_predictions(input_data):
    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)
    pred_result = model.predict(input_array_scaled)

    prob_drizzle = round(model.predict_proba(input_array_scaled)[0][0], 2)
    prob_rain = round(model.predict_proba(input_array_scaled)[0][1], 2)
    prob_sun = round(model.predict_proba(input_array_scaled)[0][2], 2)
    prob_snow = round(model.predict_proba(input_array_scaled)[0][3], 2)
    prob_fog = round(model.predict_proba(input_array_scaled)[0][4], 2)

    st.markdown("### Weather Prediction ✅")
    st.write("<span class='diagnosis-label'>Machine Learning Model Result:</span>",  unsafe_allow_html=True)
    
    if pred_result == 0:
        st.write("<span class='diagnosis drizzle'>Drizzle</span>", unsafe_allow_html=True)
    elif pred_result == 1:
        st.write("<span class='diagnosis rain'>Rain</span>", unsafe_allow_html=True)
    elif pred_result == 2:
        st.write("<span class='diagnosis sun'>Sun</span>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("Probability:", f"{prob_drizzle}%", "Drizzle")
    
    with col2:
        st.metric("Probability:", f"{prob_rain}%", "Rain")
    
    with col3:
        st.metric("Probability:", f"{prob_sun}%", "Sun")

def main():
    st.set_page_config(
        page_title="Community Based Weather Forecasting System",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with open("assets/style.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    input_data = add_sidebar()

    with st.container():
        st.title("Community Based Weather Forecasting System")
        st.write("CASE STUDY: Geidam Local Government")
        st.write("BY: BAKURA ABDULKARIM (U/CS/19/101)")
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        add_predictions(input_data)

if __name__ == "__main__":
    main()
