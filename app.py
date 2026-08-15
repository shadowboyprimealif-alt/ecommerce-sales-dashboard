from __future__ import annotations

import streamlit as st

from dashboard.page import render_page
from src import config

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="📊",
    layout="wide",
)

render_page()