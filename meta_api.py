import os
import logging
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

APP_ID = os.getenv("FB_APP_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")
ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

def validate_env():
    missing = [var for var in [APP_ID, APP_SECRET, ACCESS_TOKEN, AD_ACCOUNT_ID] if not var]
    if missing:
        raise ValueError("Beberapa variabel lingkungan tidak ditemukan. Periksa file .env Anda.")

def get_ads_data():
    logger.info("Mengambil data iklan dari Facebook Ads API...")
    validate_env()
    try:
        FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
        account = AdAccount(AD_ACCOUNT_ID)
        ads = account.get_ads(fields=[
            'name', 'campaign_name',
            'insights.metric(impressions,clicks,ctr,spend)'
        ])

        data = []
        for ad in ads:
            insights = ad.get("insights", [])
            if not insights:
                continue

            metrics = insights[0]
            spend = float(metrics.get('spend', 0))
            impressions = int(metrics.get('impressions', 0))
            clicks = int(metrics.get('clicks', 0))
            ctr = float(metrics.get('ctr', '0').replace('%',''))

            # Dummy ROAS hanya jika diperlukan
            roas = round((clicks / impressions) * 3 if impressions else 1.0, 2)

            data.append({
                'ad_name': ad['name'],
                'campaign_name': ad['campaign_name'],
                'impressions': impressions,
                'clicks': clicks,
                'ctr': ctr,
                'spend': spend,
                'roas': roas,
                'return': spend * roas
            })

        logger.info(f"Berhasil mengambil {len(data)} data iklan.")
        return pd.DataFrame(data)

    except FacebookRequestError as e:
        logger.error(f"Kesalahan API Facebook: {e}")
        raise RuntimeError(f"Kesalahan API Facebook: {e}")
    except Exception as e:
        logger.error(f"Gagal mengambil data iklan: {e}")
        raise RuntimeError(f"Gagal mengambil data iklan: {e}")