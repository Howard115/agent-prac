from streamlit_js_eval import get_geolocation
import streamlit as st
from geopy.geocoders import Nominatim

if 'count' not in st.session_state:
    st.session_state.count = 0
if 'location_obtained' not in st.session_state:
    st.session_state.location_obtained = False

st.title("Location Finder")

@st.fragment
def get_user_location():
    if not st.session_state.location_obtained:
        user_latitude_and_longitude = get_geolocation()
        
        if user_latitude_and_longitude is not None:
            st.session_state.location_obtained = True
            st.session_state.user_coords = user_latitude_and_longitude
            st.rerun(scope="fragment")
        else:
            st.warning("Waiting for location access... Please enable location access to continue")
            st.empty()  # This creates a placeholder that will be updated on rerun
    else:
        # Use the stored coordinates
        user_latitude_and_longitude = st.session_state.user_coords
        
        if st.button("Show My Location"):
            st.write(user_latitude_and_longitude)
            geolocator = Nominatim(user_agent="this is a test")
            user_location = geolocator.reverse(f'{user_latitude_and_longitude["coords"]["latitude"]}, {user_latitude_and_longitude["coords"]["longitude"]}')
            st.write(user_location)
get_user_location()
