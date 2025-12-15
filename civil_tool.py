import streamlit as st
import requests
from geopy.geocoders import Nominatim
import pandas as pd

# --- FUNCTION 1: THE LOGIC (Freeze/Thaw Calculation) ---
def count_crossings(temperatures):
    count = 0
    # Loop through the list up to the second-to-last item
    for i in range(len(temperatures) - 1):
        current_temp = temperatures[i]
        next_temp = temperatures[i+1]
        
        # Check if the line crosses zero (freeze or thaw)
        if (current_temp > 0 and next_temp < 0) or (current_temp < 0 and next_temp > 0):
            count += 1
    return count

# --- FUNCTION 2: THE DATA FETCHING (With Debugging) ---
def get_real_weather(city_name, start_date, end_date):
    # Convert dates to string format
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Sanity Check: Prevent user from putting Start Date after End Date
    if start_date > end_date:
        st.error("⚠️ Error: Start Date cannot be after End Date.")
        return None
    try:
        # 1. Get Coordinates
        geolocator = Nominatim(user_agent="civil_eng_app_v2")
        location = geolocator.geocode(city_name)
        
        if not location:
            st.error("City not found. Please check spelling.")
            return None
            
        lat = location.latitude
        lon = location.longitude
        
        # 2. Get Data from Open-Meteo API (Archive)
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date_str}&end_date={end_date_str}&hourly=temperature_2m"
        
        response = requests.get(url)
        data = response.json()
        
        # --- DEBUG CHECK ---
        # If the API returns an error instead of data, print it so we can see why.
        if 'hourly' not in data:
            st.error("⚠️ The Weather API returned an error:")
            st.json(data) # This prints the specific error reason to the screen
            return None
        # 3. Return the list of temperatures
        return data['hourly']['temperature_2m']
        
    except Exception as e:
        st.error(f"System Error: {e}")
        return None

# --- PART 3: THE WEBSITE UI ---
st.title("Real-World Freeze-Thaw Analyzer")
st.write("*Analyzes historical weather data to detect freeze-thaw cycles (temperatures measured in Celsius)*")

city = st.text_input("Enter City Name", value="Chicago")

# Columns for layout
col1, col2 = st.columns(2)

# Set SAFE default dates (Jan 2023)
with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-31"))

if st.button("Analyze Real Data", type="primary"):
    
    with st.spinner(f"Downloading weather history for {city}..."):
        real_temps = get_real_weather(city, start_date, end_date)
        
        if real_temps:
            # Run the logic
            cycles = count_crossings(real_temps)
            
            # Display results
            st.success(f"✅ Analysis Complete!")
            st.metric("Freeze-Thaw Cycles Detected", cycles)
            st.info(f"Analyzed {len(real_temps)} hourly temperature readings")
            
            # Optional: Show temperature stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min Temp (°C)", f"{min(real_temps):.1f}")
            with col2:
                st.metric("Max Temp (°C)", f"{max(real_temps):.1f}")
            with col3:
                st.metric("Avg Temp (°C)", f"{sum(real_temps)/len(real_temps):.1f}")