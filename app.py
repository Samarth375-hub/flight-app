import numpy as np
import streamlit as st
import pandas as pd
import pickle


pd.set_option('future.no_silent_downcasting',True)

with open('Flight_model.pkl', 'rb') as model_file:
    FFP = pickle.load(model_file)

with open('Features_names_original.pkl', 'rb') as feature_file:
    feature_names = pickle.load(feature_file)

st.title('Flight Price Prediction')
st.markdown('Enter the details of your flight.')

def get_user_inputs():

    col1, col2 = st.columns([4,4],gap = 'large')
    with col1:
        Source = st.selectbox('Source', ['Delhi', 'Chennai', 'Mumbai', 'Kolkata', 'Cochin'])
    with col2:
        Destination = st.selectbox('Destination', ['Hyderabad', 'Delhi', 'Mumbai', 'Kolkata', 'Cochin', 'New Delhi'])



    col1, col2 = st.columns([4, 4],gap = 'large')
    with col1:
        departure_date = st.date_input('Departure Date')
    with col2:
        dep_time = st.time_input('Departure Time')

    col1, col2 = st.columns([4, 4], gap = 'large')
    with col1:
        arrival_date = st.date_input('Arrival Date')
    with col2:
        arrival_time = st.time_input('Arrival Time')

    col1, col2 = st.columns([4,4], gap = 'large')
    with col1:
        Airline = st.selectbox('Select airline',
                               ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 'SpiceJet', 'Vistara',
                                'Air Asia', 'GoAir', 'Multiple carriers Premium economy', 'Vistara Premium economy',
                                'Jet Airways Business'])
    with col2:
        stopage = st.number_input('Number of Stops', min_value=0, max_value=4, step=1, value=0)


    Journey_day = departure_date.day
    Journey_month = departure_date.month
    Dep_hour = dep_time.hour
    Dep_min = dep_time.minute

    Arrival_hour = arrival_time.hour
    Arrival_min = arrival_time.minute

    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)

    user_data = {
        'Source': Source,
        'Destination': Destination,
        'Airline': Airline,
        'Journey_day': Journey_day,
        'Journey_month': Journey_month,
        'Dep_hour': Dep_hour,
        'Dep_min': Dep_min,
        'Arrival_hour': Arrival_hour,
        'Arrival_min': Arrival_min,
        'Duration_hours': dur_hour,
        'Duration_min': dur_min,
        'Total_Stops': stopage
    }

    features = pd.DataFrame(user_data, index=[0])

    # Apply get_dummies to the entire DataFrame at once
    features = pd.get_dummies(features, columns=['Source', 'Destination', 'Airline'], drop_first=True)

    # Ensure the feature DataFrame has the same columns as feature_names
    total = pd.DataFrame(columns=feature_names)
    total = pd.concat([total, features], axis=0)
    total = total.fillna(0)

    return total

user_input = get_user_inputs()
# st.write('User Inputs:')
# st.write(user_input)

st.markdown("""
    <style>
    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Center the button using Streamlit's container
st.markdown('<div class="center-button">', unsafe_allow_html=True)
if st.button("Predict Price"):
    fare_prediction = FFP.predict(user_input)
    st.success(f'Your Flight Price is Rs. {fare_prediction[0]:.2f}')
st.markdown('</div>', unsafe_allow_html=True)

# if st.button('Predict Price'):
#     fare_prediction = FFP.predict(user_input)
#     st.success(f'Predicted fare: Rs {fare_prediction[0]:.2f}')








