import streamlit as st

import pandas as pd
import numpy as np
import folium

import streamlit as st
from streamlit_folium import folium_static
import folium

dataset_path ='dataset/Restaurant_Scores_-_LIVES_Standard.csv'
restaurant_dataset = pd.read_csv(dataset_path)
restaurant_dataset.info()
restaurant_dataset['violation_id'] = restaurant_dataset.violation_id.str.split('_').str[2]
#replacing typos to null values as postal code is not known
replace_ca_value = dict.fromkeys(['CA', 'Ca', '941'], np.nan)
restaurant_dataset = restaurant_dataset.replace(replace_ca_value)
#making postal code in symmetry with 5 digits only
restaurant_dataset.business_postal_code = restaurant_dataset.business_postal_code.str[:5]

restaurant_dataset=restaurant_dataset.dropna(subset=['Supervisor Districts','business_postal_code','inspection_score'])
restaurant_dataset = restaurant_dataset.dropna(axis=0, subset=['business_longitude', 'violation_description'])
restaurant_dataset=restaurant_dataset.dropna(subset=['risk_category'])
#take only date and not time
#restaurant_dataset['inspection_date'] = restaurant_dataset['inspection_date'].str[:10]
restaurant_dataset['inspection_date_p'] = pd.to_datetime(restaurant_dataset['inspection_date'])



"# streamlit-folium"
SF_COORDINATES = (37.76, -122.45)
with st.echo():
    import streamlit as st
    from streamlit_folium import folium_static
    import folium
    map = folium.Map(location=SF_COORDINATES, zoom_start=12) 

# add a marker for every record in the filtered data, use a clustered view
    for each in restaurant_dataset[:100].iterrows():
        if each[1]["risk_category"]=='High Risk':
            folium.Marker([each[1]["business_latitude"],
                           each[1]["business_longitude"]],
                          popup=each[1]["business_name"].replace("'", "") + " Violation: " + each[1]["violation_description"],icon=folium.Icon(color='green')).add_to(map)
        elif each[1]["risk_category"]=='Low Risk' :
            folium.Marker([each[1]["business_latitude"],
                           each[1]["business_longitude"]],
                          popup=each[1]["business_name"].replace("'", "") + " Violation: " + each[1]["violation_description"],icon=folium.Icon(color='red')).add_to(map)

        else:
            folium.Marker([each[1]["business_latitude"],
                           each[1]["business_longitude"]],
                          popup=each[1]["business_name"].replace("'", "") + " Violation: " + each[1]["violation_description"],icon=folium.Icon(color='blue')).add_to(map)


   
    # call to render Folium map in Streamlit
    folium_static(map)