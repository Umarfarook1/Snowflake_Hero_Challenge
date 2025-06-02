import streamlit as st
import pandas as pd
import pydeck as pdk
from snowflake.snowpark import Session

SNOWFLAKE_ACCOUNT=FZGJWGR-FW92534
SNOWFLAKE_USER=Umarfarook
SNOWFLAKE_PASSWORD=Umarfarook@112002
SNOWFLAKE_AUTHENTICATOR=snowflake
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=HERO_CHALLEGE
SNOWFLAKE_SCHEMA=PUBLIC


st.set_page_config(page_title="Incredible India – Cultural Explorer", layout="wide")

# --------------------
# Snowflake session
# --------------------

@st.cache_resource(show_spinner=False)
def get_snowflake_session():
    try:
        connection_parameters = {
            "account": SNOWFLAKE_ACCOUNT,
            "user": SNOWFLAKE_USER,
            "password": SNOWFLAKE_PASSWORD,
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA
        }
        
        session = Session.builder.configs(connection_parameters).create()
        return session
    except Exception as e:
        st.error(f"❌ Failed to connect to Snowflake: {str(e)}")
        raise Exception(f"Failed to connect to Snowflake: {str(e)}")

session = get_snowflake_session()

# --------------------
# Data loading helpers
# --------------------

@st.cache_data(show_spinner=False)
def load_foods():
    if session is None:
        return pd.DataFrame()
    return session.table("FOODS").to_pandas()

@st.cache_data(show_spinner=False)
def load_festivals():
    if session is None:
        return pd.DataFrame()
    return session.table("FESTIVALS").to_pandas()

@st.cache_data(show_spinner=False)
def load_tourist_places():
    if session is None:
        return pd.DataFrame()
    return session.table("TOURIST_PLACES").to_pandas()

# --------------------
# Page functions
# --------------------

def footer():
    st.markdown(
        """
        <hr>
        <p style="font-size:12px; text-align:center; color:gray;">
        Built with ❤️ for Hero Challenge 2025 | Powered by Streamlit & Snowflake
        </p>
        """, unsafe_allow_html=True
    )

def show_home():
    st.title("🇮🇳 Incredible India – Cultural Explorer")

    st.markdown(
        """
        ### ✨ About the App
        Welcome to **Incredible India – Cultural Explorer**, a visual journey through India’s rich cultural tapestry. Here’s what you can explore:

        🥜 **Food**  
        Explore regional dishes from North, South, East, and West India. View food names, descriptions, and drool-worthy images.

        🚩 **Tourist Places**  
        Discover the top 3 tourist attractions in every state. See all locations on a map. Zoom into a state to see all its places. Click markers to view detailed info.

        🎉 **Festivals**  
        Browse important festivals celebrated in each state with beautiful descriptions and dates.

        ---
        """
    )
    try:
        food_df = load_foods()
        festivals_df = load_festivals()
        places_df = load_tourist_places()

        # Use STATE_NAME uniformly for union sets
        states_set = set()
        if 'STATE_NAME' in festivals_df.columns:
            states_set.update(festivals_df['STATE_NAME'].dropna().unique())
        if 'STATE_NAME' in food_df.columns:
            states_set.update(food_df['STATE_NAME'].dropna().unique())
        if 'STATE_NAME' in places_df.columns:
            states_set.update(places_df['STATE_NAME'].dropna().unique())

        total_states = len(states_set)
        total_festivals = len(festivals_df)
        total_foods = len(food_df)
        total_places = len(places_df)

        st.subheader("📊 Cultural Snapshot")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🚩 States Covered", total_states)
        col2.metric("🎉 Festivals", total_festivals)
        col3.metric("🍛 Dishes", total_foods)
        col4.metric("📍 Tourist Places", total_places)

        st.markdown("---")
        st.markdown(
            """
            ### 🧯 Navigate Further
            Use the **sidebar** to explore:
            - 🥘 **Food** – Dive into Indian cuisine
            - 🎆 **Festivals** – Discover vibrant celebrations
            - 🌄 **Tourist Places** – Plan your cultural journey
            """
        )
    except Exception as e:
        st.error("⚠️ Error loading data or displaying statistics.")
        st.exception(e)
    footer()


def show_food_page():
    st.title("🍲 Indian Cuisine Explorer")
    st.markdown("Explore the diverse and delicious cuisines of India, categorized by region. 🇮🇳")

    try:
        df = load_foods()
        if df.empty:
            st.warning("No food data available.")
            footer()
            return

        for region in sorted(df["REGION"].dropna().unique()):
            st.markdown("---")
            st.subheader(f"📍 {region} India")

            region_df = df[df["REGION"] == region]

            for _, row in region_df.iterrows():
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #eee;">
                            <h5 style="margin-bottom:5px;">🍛 {row['FOOD_NAME']}</h5>
                            <p style="margin:0; color:#555;">{row['DESCRIPTION']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
    except Exception as e:
        st.error("⚠️ Could not load food data.")
        st.exception(e)
    footer()


def show_festivals_page():
    st.title("🎉 Festivals of India")
    st.markdown(
        "Experience the rich cultural heritage of India through its diverse festivals celebrated across different states."
    )

    try:
        df = load_festivals()
        if df.empty:
            st.warning("No festival data available.")
            footer()
            return

        # Sorting by DATE, assuming DATE is a string or datetime type
        if 'DATE' in df.columns:
            try:
                df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                df = df.sort_values(by='DATE')
            except Exception:
                pass  # Keep original if parsing fails

        search_query = st.text_input("🔍 Search by festival or state name").lower()

        if search_query:
            df = df[
                df['FESTIVAL_NAME'].str.lower().str.contains(search_query)
                | df['STATE_NAME'].str.lower().str.contains(search_query)
            ]

        if df.empty:
            st.warning("No festivals match your search. Try a different name or state.")
            footer()
            return

        for _, row in df.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div style="border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem; background-color: #fff8dc; border-left: 8px solid #ff7f50;">
                        <h3 style="margin-bottom: 0.5rem;">🎊 {row['FESTIVAL_NAME']}</h3>
                        <p style="margin: 0.3rem 0;"><strong>📍 State:</strong> {row['STATE_NAME']}</p>
                        <p style="margin: 0.3rem 0;"><strong>📅 Date:</strong> {row['DATE'].strftime('%Y-%m-%d') if pd.notnull(row['DATE']) else row['DATE']}</p>
                        <p style="margin-top: 1rem;">{row['DESCRIPTION']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    except Exception as e:
        st.error("⚠️ Could not load festivals data.")
        st.exception(e)
    footer()


def show_tourist_places_page():
    st.title("🗺️ Discover Attractions")

    try:
        with st.spinner("Loading tourist attractions..."):
            df = load_tourist_places()

        if df.empty:
            st.warning("No tourist places data available.")
            footer()
            return

        required_cols = ['LONGITUDE', 'LATITUDE', 'PLACE_NAME', 'DESCRIPTION']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            footer()
            return

        df_clean = df.dropna(subset=['LONGITUDE', 'LATITUDE'])
        invalid_coords = len(df) - len(df_clean)
        if invalid_coords > 0:
            st.info(f"Filtered out {invalid_coords} places with invalid coordinates.")

        if df_clean.empty:
            st.warning("No places with valid coordinates found.")
            footer()
            return

        st.sidebar.subheader("🔍 Filters")

        search_term = st.sidebar.text_input("Search places:", placeholder="Enter place name...")
        df_filtered = df_clean

        if search_term:
            df_filtered = df_filtered[df_filtered['PLACE_NAME'].str.contains(search_term, case=False, na=False)]

        # Use STATE_NAME if present, else fallback to STATE
        state_col = 'STATE_NAME' if 'STATE_NAME' in df_clean.columns else 'STATE' if 'STATE' in df_clean.columns else None

        if state_col:
            states = ['All'] + sorted(df_clean[state_col].dropna().unique().tolist())
            selected_state = st.sidebar.selectbox("Select State:", states)
            if selected_state != 'All':
                df_filtered = df_filtered[df_filtered[state_col] == selected_state]

        if df_filtered.empty:
            st.warning("No places match your filters. Try adjusting your search criteria.")
            footer()
            return

        center_lat = df_filtered['LATITUDE'].mean()
        center_lon = df_filtered['LONGITUDE'].mean()

        lat_range = df_filtered['LATITUDE'].max() - df_filtered['LATITUDE'].min()
        lon_range = df_filtered['LONGITUDE'].max() - df_filtered['LONGITUDE'].min()
        max_range = max(lat_range, lon_range)

        zoom_level = 8
        if max_range > 10:
            zoom_level = 3
        elif max_range < 1:
            zoom_level = 10
        elif max_range < 3:
            zoom_level = 7

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom_level,
            pitch=0,
            bearing=0,
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_filtered,
            get_position='[LONGITUDE, LATITUDE]',
            get_fill_color=[255, 0, 0, 180],
            get_radius=1000,
            radius_min_pixels=5,
            radius_max_pixels=10,
            pickable=True,
            auto_highlight=True,
        )

        tooltip = {
            "html": "<b>{PLACE_NAME}</b><br/>{DESCRIPTION}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white",
                "fontSize": "14px",
                "padding": "10px",
                "borderRadius": "5px",
            },
        }

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=view_state,
                layers=[layer],
                tooltip=tooltip,
            )
        )
    except Exception as e:
        st.error("⚠️ Error loading or displaying tourist places.")
        st.exception(e)
    footer()


# --------------------
# Main app navigation
# --------------------

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Food", "Festivals", "Tourist Places"])

if page == "Home":
    show_home()
elif page == "Food":
    show_food_page()
elif page == "Festivals":
    show_festivals_page()
elif page == "Tourist Places":
    show_tourist_places_page()
