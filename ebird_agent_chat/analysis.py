import streamlit as st
import pandas as pd
from fetch_img import initialize_browser, fetch_img
from get_observation import get_nearby_bird_observations
from urllib.parse import quote



# Load and process the data

def load_data():
    data = get_nearby_bird_observations()
    if data is None:
        st.rerun()
    
    # Create a list to store flattened observations
    rows = []
    for obs in data:
        row = {
            'locId': obs['locId'],
            'locName': obs['locName'],
            'speciesCode': obs['speciesCode'],
            'comName': obs['comName'],
            'sciName': obs['sciName'],
            'obsDt': obs['obsDt'],
            'howMany': obs['howMany']
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Create location summary with species list
    location_species = df.groupby('locName')['comName'].agg(lambda x: ', '.join(sorted(set(x)))).reset_index()
    location_species.columns = ['Location', 'Species Present']
    
    return df, location_species

# Create the Streamlit app
st.title('Bird Observation Analysis')

# Initialize session state variables
if 'location_obtained' not in st.session_state:
    st.session_state.location_obtained = False

if 'browser_driver' not in st.session_state:
    st.session_state.browser_driver = initialize_browser()

if 'df' not in st.session_state:
    st.session_state.df, st.session_state.location_summary = load_data()

st.subheader('Species Present at Each Location')

# Add Google Maps direction link
locations = st.session_state.location_summary['Location'].tolist()
if locations:
    # URL encode location names (handles international characters)
    formatted_locations = [quote(loc) for loc in locations]
    
    # Use the last location as destination and others as waypoints
    destination = formatted_locations[-1]
    waypoints = '|'.join(formatted_locations[:-1]) if len(formatted_locations) > 1 else ''
    
    maps_url = f"https://www.google.com/maps/dir/?api=1&waypoints={waypoints}&destination={destination}&travelmode=driving"
    st.markdown(f"[View Route on Google Maps]({maps_url})")

# Create an interactive display for the location summary
for _, row in st.session_state.location_summary.iterrows():
    with st.container():
        st.write(f"📍 {row['Location']}")
        species_list = row['Species Present'].split(', ')
        
        # Create columns for species popovers (5 species per row)
        cols = st.columns(5)
        for idx, species in enumerate(species_list):
            with cols[idx % 5]:
                # Get species details from the main dataframe
                species_data = st.session_state.df[
                    st.session_state.df['comName'] == species
                ]
                species_code = species_data['speciesCode'].iloc[0]
                
                with st.popover(f"{species}"):
                    # Show observation details first
                    st.write("**Recent Observations:**")
                    for _, obs in species_data.iterrows():
                        st.write(f"{obs['obsDt']}: {obs['howMany']} birds")
                    
                    # Create a unique key for storing the image
                    img_key = f"img_{species_code}"
                    if img_key not in st.session_state:
                        st.session_state[img_key] = None
                    
                    # Show button only if image hasn't been loaded yet
                    if st.session_state[img_key] is None:
                        if st.button(f"Load image for {species}", key=f"btn_{species_code}"):
                            try:
                                img_data = fetch_img(st.session_state.browser_driver, species_code)
                                st.session_state[img_key] = img_data
                            except Exception as e:
                                st.session_state[img_key] = f"Error: {str(e)}"
                    
                    # Display image if it has been loaded
                    if st.session_state[img_key] is not None:
                        if isinstance(st.session_state[img_key], str) and st.session_state[img_key].startswith("Error"):
                            st.error(st.session_state[img_key])
                        else:
                            st.image(st.session_state[img_key])
        st.divider()  # Add a visual separator between locations



# Add download button
csv = st.session_state.location_summary.to_csv(index=False)
st.download_button(
    label="Download Location Summary as CSV",
    data=csv,
    file_name="location_summary.csv",
    mime="text/csv",
)