
Incredible India – Cultural Explorer
=====================================

This is a Streamlit web application that offers an interactive exploration of India’s rich cultural heritage. The app connects to a Snowflake database to fetch and display curated data on Indian regional foods, famous festivals, and top tourist places across different states.

Features
--------

* **Home Page**:Provides an overview of the app, including quick stats about the number of states covered, festivals, dishes, and tourist places featured.
* **Food Page**:Explore diverse Indian cuisine categorized by region (North, South, East, West). Each dish shows its name and a brief description.
* **Festivals Page**:Browse through India’s vibrant festivals by state, with festival names, descriptions, and dates. Includes a search option for easy filtering.
* **Tourist Places Page**:Discover top tourist attractions across India with interactive maps. You can filter places by state or search by name. Clicking on map markers shows detailed info about each location.

Technologies Used
-----------------

* **Streamlit** for building the interactive web app with an easy-to-use interface.
* **Snowflake** as the cloud data warehouse to store and query the cultural data.
* **Snowpark Python API** to connect Streamlit with Snowflake for data loading.
* **Pydeck** to render interactive maps showing tourist places on the map.

Getting Started
---------------

1. Clone the repository.
2. Create a .env file with your Snowflake account credentials.
3. Install dependencies (e.g., streamlit, snowflake-snowpark-python, pandas, pydeck).
4. Run the app locally with streamlit run app.py.

Data Source
-----------

The app uses custom Snowflake tables named FOODS, FESTIVALS, and TOURIST\_PLACES, which contain data on Indian culture, cuisine, celebrations, and attractions.

Purpose
-------

This project aims to provide a simple and visually appealing way for users to learn about India’s diverse cultural landscape, helping travelers, students, and culture enthusiasts discover new and exciting aspects of the country.
