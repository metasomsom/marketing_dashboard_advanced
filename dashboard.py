import streamlit as st
import plotly.express as px
from meta_api import get_ads_data
import openai
import pandas as pd
import io
import os
from dotenv import load_dotenv
from utils import (
    load_and_cache_data,
    display_campaign_metrics,
    display_ad_charts,
    download_filtered_data,
    generate_ad_copy
)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Meta Ads Dashboard", layout="wide")
st.title("📊 Dashboard Meta Ads")

# Load and cache data
data = load_and_cache_data()

if data.empty:
    st.warning("Tidak ada data ditemukan.")
else:
    campaigns = data['campaign_name'].unique()
    selected_campaign = st.selectbox("🎯 Pilih Kampanye", campaigns)
    filtered_data = data[data['campaign_name'] == selected_campaign]

    display_campaign_metrics(filtered_data)
    st.subheader("📋 Data Iklan")
    st.dataframe(filtered_data)

    display_ad_charts(filtered_data)
    download_filtered_data(filtered_data)

    st.subheader("🧠 Generator Iklan AI")
    product = st.text_input("Masukkan Nama Produk")
    if st.button("Buat Copy Iklan"):
        if product.strip():
            with st.spinner("Membuat teks iklan..."):
                copy = generate_ad_copy(product)
                st.text_area("📝 Hasil Copy Iklan:", copy, height=200)
        else:
            st.warning("Masukkan nama produk terlebih dahulu.")
