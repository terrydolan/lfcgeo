#!/usr/bin/env python
# coding: utf-8
"""
lfcgeo App

A python streamlit web app that maps each LFC squad player's shortest journey
from their place of birth to Anfield for a selected season

To run:
    $streamlit run lfcgeo_app.py

History
v1.0.0 - Sep 2020, Initial version with python, pandas, ast, pydeck and
         streamlit
V1.1.0 - June 2023, Update the supporting library versions; add read of 
         encrypted csv using cryptography module and streamlit secrets;
         improve page flow using streamlit session state; moved from heroku 
         to streamlit community cloud 
         
"""


import logging
import logging.config
import ast
from io import BytesIO

import cryptography as crp # required only for error codes
import pydeck as pdk
import pandas as pd
import streamlit as st

import crypto_utils # local cryptographic helper functions
import lfcgeo_log_config # dict with logging config

__author__ = "Terry Dolan"
__copyright__ = "Terry Dolan"
__license__ = "MIT"
__email__ = "terrydolan1892@gmail.com"
__status__ = "Beta"
__version__ = "1.1.0"
__updated__ = "June 2023"

# ---------------------------------------------------------------------------
# set up

# set up logging
logging.config.dictConfig(lfcgeo_log_config.dictLogConfig)
logger = logging.getLogger('lfcgeo')

# define defaults
MODE_RUN = 'Run the lfcgeo app'
MODE_ABOUT = 'About the lfcgeo app'
MODE_ANI = 'Run the PTWR animation'
SHOW_DATAFRAME = True

# define map data
ANFIELD_LATITUTE = 53.4308358
ANFIELD_LONGITUDE = -2.9609095414165294
DEFAULT_SEASON = '1900-1901' # Liverpool's first title winning season
ZOOM_ANFIELD = 11
ZOOM_WORLD = 0.6
ZOOM_DEFAULT = 4
GREEN = [0, 255, 0] # RGB
RED = [255, 0, 0] # RGB
WHITE = [255, 255, 255] # RGB
LINE_WIDTH=7
PICKING_RADIUS = 5*LINE_WIDTH
# ref: https://docs.mapbox.com/api/maps
MAP_STYLE = 'mapbox://styles/mapbox/dark-v10'

# set initial map view values
view_zoom_level = ZOOM_DEFAULT
view_latitude = ANFIELD_LATITUTE
view_longitude = ANFIELD_LONGITUDE

# define app data files
# note that latest version of the app uses the encrypted csv
SQUAD_PLAYERS_GEO_CSV_FILE = 'data/dflfc_squad_players_geo_Sep2020.csv'
SQUAD_PLAYERS_GEO_CSV_FILE_ENCRYPTED = (
    'data/dflfc_squad_players_geo_Sep2020.enc')
ABOUT_MD_FILE = 'README.md'
ANI_GIF = "LFC PTWR 1892-1893 to 2020-2021.gif"
ANI_MP4 = "LFC PTWR 1892-1893 to 2020-2021.mp4"

# ---------------------------------------------------------------------------
# define helper functions

@st.cache_resource
def decrypy_and_read_lfcgeo_df():
    """Decrypt csv with squad players geo data and return as a dataframe."""
    logger.info("Decrypt csv using key and load dataframe")
    try:
        decrypted_file_bytes = BytesIO(
            crypto_utils.decrypt_to_bytes(SQUAD_PLAYERS_GEO_CSV_FILE_ENCRYPTED,
                                          st.secrets["key"].encode()))
        df = pd.read_csv(decrypted_file_bytes, parse_dates=['Birthdate'])
    except (crp.fernet.InvalidToken, TypeError, KeyError):
        st.error("Failed to decrypt dataframe, check key")
        st.stop()
    # print(f"dataframe head:\n: {df.head()}")
    return df

@st.cache_data
def read_lfcgeo_df():
    """Read csv with squad players geo data and return as a dataframe."""
    logger.info("Load dataframe")
    df = pd.read_csv(SQUAD_PLAYERS_GEO_CSV_FILE, parse_dates=['Birthdate'])
    # print(f"dataframe head:\n: {df.head()}")
    return df

@st.cache_data
def read_about_md(filename):
    """Read the about markdown file and return as a string."""
    with open(filename, "r") as f:
        about_md = f.read()
    return about_md

def show_season_map(dflfc_squad_player_geo, selected_season):
    """Show season map."""
    logger.info(f"Show season map for selected season: {selected_season}")
    # print(f"show_season_map: {selected_season=}")

    # filter selected season in dataframe and prepare dataframe for mapping
    FILTER = dflfc_squad_player_geo.Season == selected_season
    df_plot = dflfc_squad_player_geo[FILTER].dropna().reset_index(drop=True)
    df_plot['Source_coords_xfm'] = (
        df_plot.Source_coords_xfm.apply(lambda s: tuple(ast.literal_eval(s))))
    df_plot['Target_coords'] = (
        df_plot.Target_coords.apply(lambda s: tuple(ast.literal_eval(s))))
    df_plot['Anfield_dist_mi_rnd'] = round(df_plot.Anfield_dist_mi, 1)

    # map using great circle layer
    layer = pdk.Layer(
         "GreatCircleLayer",
         df_plot,
         pickable=True,
         # column in dataframe with source (birthplace) coordinates (x, y)
         get_source_position='Source_coords_xfm',
         # column in dataframe with target (Anfield) coordinates (x, y)
         get_target_position='Target_coords',
         get_source_color=GREEN,
         get_target_color=RED,
         auto_highlight=True,
         get_width=LINE_WIDTH,
         picking_radius=PICKING_RADIUS,
         highlightColor=WHITE
         )

    # set the viewport location
    view_state = pdk.ViewState(latitude=view_latitude,
                                longitude=view_longitude,
                                zoom=view_zoom_level,
                                bearing=0,
                                pitch=0)

    # render
    logger.info(f"Render the lfcgeo map for season: {selected_season}")
    r = pdk.Deck(layers=[layer],
                  initial_view_state=view_state, map_style=MAP_STYLE,
                  tooltip={"text": "{Player}\n\
                          from {Birthplace_upd}\n\
                              to Anfield ({Anfield_dist_mi_rnd} miles)"})
    r.picking_radius=2*PICKING_RADIUS

    # show the rendered chart
    st.write((
        f"{selected_season} - the map is interactive, hover over a line to "
        f"see player details; zoom in and out"))
    st.pydeck_chart(r)
    st.markdown("_Data source: [lfchistory.net](https://www.lfchistory.net/)_")

def show_season_data(dflfc_squad_player_geo, selected_season):
    """Show season data."""
    # print(f"show_season_data: {selected_season=}")
    logger.info(f"Show season data for selected season: {selected_season}")

    # filter selected season in dataframe and prepare dataframe for display
    FILTER = dflfc_squad_player_geo.Season == selected_season
    df_plot = dflfc_squad_player_geo[FILTER].dropna().reset_index(drop=True)

    # show the data
    st.write((
        df_plot[['Season', 'Player', 'Birthplace_upd',
                  'Source_coords_xfm']]\
              .rename(columns={'Birthplace_upd': 'Birthplace',
                              'Source_coords_xfm': 'Geo-location'})\
              .astype(str)))

# ---------------------------------------------------------------------------
# define page config
st.set_page_config(
    page_title="lfcgeo",
    page_icon="redglider.ico",
    layout="wide",
    initial_sidebar_state="auto") #collapsed expanded

# ---------------------------------------------------------------------------
# define sidebar to select mode (default mode is to run the app)
select_mode = st.sidebar.radio('Select mode:',
                               (MODE_RUN, MODE_ABOUT, MODE_ANI), index=0)

st.sidebar.markdown(f"*lfcgeo, version {__version__}*")

# ---------------------------------------------------------------------------
# define pages for modes
if select_mode == MODE_RUN:

    # introduce the web app
    st.title("lfcgeo")
    st.header("Map each LFC squad player's shortest journey from their \
              birthplace to Anfield")

    # load (once) the dataframe
    dflfc_squad_player_geo = decrypy_and_read_lfcgeo_df()

    # read (once) all squad players' data, with geo and tooltip
    if 'seasons' not in st.session_state:
        # print("set seasons")
        logger.info('Set the seasons')
        st.session_state.seasons = list(dflfc_squad_player_geo.Season.unique())


    # select season using slider
    st.select_slider(label='Select a season to map using the slider:',
                      options=st.session_state.seasons,
                      value=DEFAULT_SEASON,
                      key='selected_season')

    # show map for selected season
    if st.session_state.selected_season:
        show_season_map(dflfc_squad_player_geo,
                        st.session_state.selected_season)

    # display dataframe (if required)
    if SHOW_DATAFRAME and st.session_state.selected_season:
        show_data = st.checkbox((
            f"Show data for the {st.session_state.selected_season} season"))
        if show_data:
            logger.info((
                f"Show the dataframe for season: "
                f"{st.session_state.selected_season}"))
            show_season_data(dflfc_squad_player_geo,
                             st.session_state.selected_season)

elif select_mode == MODE_ABOUT:
    logger.info('Show info about lfcgeo')
    st.markdown(read_about_md(ABOUT_MD_FILE))

elif select_mode == MODE_ANI:
    logger.info('Show PTWR animation')
    st.video(ANI_MP4)
    #st.image(ANI_GIF)
    st.markdown("_Data source: [lfchistory.net](https://www.lfchistory.net/)_")
