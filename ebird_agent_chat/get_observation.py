from ebird.api import get_nearby_observations
import streamlit as st
from streamlit_js_eval import get_geolocation

api_key = '62vrn2b53gfe'
locale = 'zh'

if 'location_obtained' not in st.session_state:
    st.session_state.location_obtained = False


def get_user_location():
    user_location = get_geolocation()
    
    if user_location is not None:
        st.session_state.location_obtained = True
        cur_lat = user_location["coords"]["latitude"]
        cur_lon = user_location["coords"]["longitude"]
        st.session_state.user_lat = cur_lat
        st.session_state.user_lon = cur_lon
        st.rerun()
    else:
        st.warning("Waiting for location access... Please enable location access to continue")
        st.empty()

@st.cache_data(ttl=60*60*24)
def get_bird_observations_by_coords(lat, lon):
    records = get_nearby_observations(
        api_key, 
        lat, 
        lon, 
        dist=15, 
        back=7,
        locale=locale,
        hotspot=True,
        max_results=100
    )
    return records


def get_nearby_bird_observations():
    if not st.session_state.location_obtained:
        get_user_location()
    else:
        user_lat, user_lon = st.session_state.user_lat, st.session_state.user_lon
        records = get_bird_observations_by_coords(user_lat, user_lon)
        return records


