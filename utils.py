import streamlit as st
import plotly.express as px
import pandas as pd
import openai
from openai import RateLimitError  # Impor langsung dari openai
import io
from functools import lru_cache
from meta_api import get_ads_data

@st.cache_data(show_spinner=False, ttl=3600)
def load_and_cache_data():
    try:
        return get_ads_data()
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

def display_campaign_metrics(filtered_data):
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spend", f"${filtered_data['spend'].sum():,.2f}")
    col2.metric("Average CTR", f"{filtered_data['ctr'].mean():.2f}%")
    col3.metric("Average ROAS", f"{filtered_data['roas'].mean():.2f}")

def display_ad_charts(filtered_data):
    st.subheader("📊 CTR per Iklan")
    fig = px.bar(filtered_data, x="ad_name", y="ctr", title="CTR per Iklan", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 ROAS per Iklan")
    fig_roas = px.bar(filtered_data, x="ad_name", y="roas", title="ROAS per Iklan", text_auto=True)
    st.plotly_chart(fig_roas, use_container_width=True)

def download_filtered_data(filtered_data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        filtered_data.to_excel(writer, index=False, sheet_name='Ads Data')
    st.download_button("📥 Download Excel", data=output.getvalue(), file_name="report_ads.xlsx")

def generate_ad_copy(product):
    try:
        response = openai.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=[
                {"role": "user", "content": f"Buatkan teks iklan menarik untuk produk '{product}'"}
            ]
        )
        return response.choices[0].message.content
    except RateLimitError:
        return "Batas kuota OpenAI tercapai. Coba lagi nanti."
    except Exception as e:
        return f"Terjadi kesalahan saat membuat teks iklan: {e}"