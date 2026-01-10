# Real-World Freeze-Thaw Analyzer
**Project Documentation & User Guide**

## 1. Project Overview
This application is a **Streamlit** dashboard designed for Civil Engineering analysis. It automates the process of identifying "freeze-thaw cycles" (critical for determining weathering risk in construction materials) using real historical weather data.

**Key Features:**
* **Geocoding:** Converts city names (e.g., "Chicago") into GPS coordinates.
* **Historical Data:** Fetches real hourly temperature data from the Open-Meteo Archive API.
* **Algorithm:** Counts how many times the temperature crosses $0^\circ C$ (freezing point) within a selected date range.
* **Statistics:** Improved Min/Max/Average temperature calculations.

## 2. Installation & Setup
If you are setting this up on a new computer, follow these steps.

### Prerequisites
* Python 3.8 or higher installed.
* An internet connection (required for the Weather API).

### Step 1: Install Libraries
Open your terminal (Command Prompt) and run the following command to install the required tools:

```bash

pip install streamlit requests geopy pandas




