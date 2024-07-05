import streamlit as st
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the trained model
@st.cache_resource
def load_trained_model():
    return load_model('incident_prediction_model.h5')

model = load_trained_model()

# State mapping
state_mapping = {
    'Connecticut': 0,
    'Maine': 1,
    'Massachusetts': 2,
    'New Hampshire': 3,
    'New Jersey': 4,
    'New York': 5,
    'Rhode Island': 6,
    'Vermont': 7
}

# Reverse mapping for display
reverse_state_mapping = {v: k for k, v in state_mapping.items()}

# Streamlit Interface
st.title('Incident Prediction')

# Date input
date = st.date_input("Select Date")
month = date.month
day = date.day

# Dropdown for state selection
state_name = st.selectbox('Select State', list(state_mapping.keys()))
state_code = state_mapping[state_name]

# Sliders for SPL and RPL themes
spl_theme1 = st.slider('SPL_THEME1', min_value=0.0, max_value=1.0, step=0.01)
rpl_theme1 = st.slider('RPL_THEME1', min_value=0.0, max_value=1.0, step=0.01)
spl_theme2 = st.slider('SPL_THEME2', min_value=0.0, max_value=1.0, step=0.01)
rpl_theme2 = st.slider('RPL_THEME2', min_value=0.0, max_value=1.0, step=0.01)
spl_theme3 = st.slider('SPL_THEME3', min_value=0.0, max_value=1.0, step=0.01)
rpl_theme3 = st.slider('RPL_THEME3', min_value=0.0, max_value=1.0, step=0.01)
spl_theme4 = st.slider('SPL_THEME4', min_value=0.0, max_value=1.0, step=0.01)
rpl_theme4 = st.slider('RPL_THEME4', min_value=0.0, max_value=1.0, step=0.01)

# Prediction button
if st.button('Predict'):
    try:
        # Create input DataFrame
        input_data = pd.DataFrame({
            'Month': [month],
            'Day': [day],
            'State': [state_code],
            'SPL_THEME1': [spl_theme1],
            'RPL_THEME1': [rpl_theme1],
            'SPL_THEME2': [spl_theme2],
            'RPL_THEME2': [rpl_theme2],
            'SPL_THEME3': [spl_theme3],
            'RPL_THEME3': [rpl_theme3],
            'SPL_THEME4': [spl_theme4],
            'RPL_THEME4': [rpl_theme4]
        })

        # Make prediction
        prediction = model.predict(input_data)[0][0]
        result = 'Incident likely' if prediction > 0.5 else 'No incident likely'

        # Display result
        st.write(f'Prediction: {result}')
        st.write(f'Prediction Probability: {prediction:.2f}')
    except Exception as e:
        st.error(f"An error occurred: {e}")
