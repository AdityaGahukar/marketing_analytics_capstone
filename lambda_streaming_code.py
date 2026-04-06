# Set Lambda environment variables:
# S3_BUCKET = your-bucket-name
# S3_PREFIX = streaming
# NUM_RECORDS = 500

from __future__ import annotations
import io
import json
import logging
import os
import random
from datetime import date, timedelta, datetime

import boto3
import pandas as pd
from faker import Faker

logger = logging.getLogger()
logger.setLevel(logging.INFO)

fake = Faker()

# ── Runtime config (env vars) ──────────────────────────────
NUM_RECORDS  = int(os.environ.get("NUM_RECORDS", 500))
S3_BUCKET    = os.environ.get("S3_BUCKET", "")         # REQUIRED
S3_PREFIX    = os.environ.get("S3_PREFIX", "streaming") # default folder

# ── Constants ─────────────────────────────────────────────
START_DATE = date(2025, 1, 1)
END_DATE   = date(2025, 3, 31)

AGE_GROUPS = ["13-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
GENDERS    = ["Male", "Female", "Unknown"]

CAMPAIGN_PREFIXES = {
    "Facebook":   ["FB_Brand_",   "FB_Retarget_",  "FB_Awareness_", "FB_Conv_"],
    "Instagram":  ["IG_Story_",   "IG_Reel_",      "IG_Collab_",    "IG_Promo_"],
    "YouTube":    ["YT_Preroll_", "YT_Bumper_",    "YT_Discovery_", "YT_Shorts_"],
    "Google Ads": ["GGL_Search_", "GGL_Display_",  "GGL_PMax_",     "GGL_Video_"],
}

_ALT_DATE_FORMATS = [
    lambda d: d.strftime("%d/%m/%Y"),
    lambda d: d.strftime("%m-%d-%Y"),
    lambda d: d.strftime("%B %d, %Y"),
    lambda d: d.strftime("%Y/%m/%d"),
    lambda d: d.strftime("%d-%b-%Y"),
]
_BAD_CURRENCY = ["usd", "US Dollar", "840", "Usd"]
_BAD_GENDER   = {
    "Male":    ["male", "MALE", "M", "m"],
    "Female":  ["female", "FEMALE", "F", "f"],
    "Unknown": ["unknown", "UNKNOWN", "N/A", "na"],
}

# ── Helper functions ──────────────────────────────────────
def _rand_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))

def _anomaly_date(d: date) -> str:
    if random.random() < 0.15:
        return random.choice(_ALT_DATE_FORMATS)(d)
    return d.strftime("%Y-%m-%d")

def _anomaly_campaign(name: str):
    r = random.random()
    if r < 0.03:
        return random.choice([None, "", "N/A"])
    if r < 0.11:
        return f"{' ' * random.randint(1,3)}{name}{' ' * random.randint(0,2)}"
    return name

def _anomaly_date_field(d: date):
    if random.random() < 0.03:
        return random.choice([None, ""])
    return _anomaly_date(d)

def _anomaly_gender(gender: str) -> str:
    if random.random() < 0.15:
        return random.choice(_BAD_GENDER[gender])
    return gender

def _anomaly_spend(spend: float) -> float:
    return -abs(spend) if random.random() < 0.02 else spend

def _anomaly_currency(code: str) -> str:
    return random.choice(_BAD_CURRENCY) if random.random() < 0.03 else code

def _anomaly_metrics(impressions, clicks, reach):
    if random.random() < 0.02:
        if random.random() < 0.5:
            clicks = impressions + random.randint(1, 500)
        else:
            reach  = impressions + random.randint(1, 1_000)
    return impressions, clicks, reach

def _anomaly_cost_micros(val: int):
    return f"{float(val)}" if random.random() < 0.05 else val

# ── Platform row builders ─────────────────────────────────
def _facebook_row() -> dict:
    impressions = random.randint(1_000, 500_000)
    reach       = int(impressions * random.uniform(0.50, 0.95))
    clicks      = random.randint(10, max(11, int(impressions * 0.05)))
    spend       = _anomaly_spend(round(random.uniform(5.0, 5_000.0), 2))
    plays_25    = int(impressions * random.uniform(0.10, 0.60))
    plays_50    = int(plays_25 * random.uniform(0.40, 0.85))
    plays_100   = int(plays_50 * random.uniform(0.30, 0.75))
    d           = _rand_date(START_DATE, END_DATE)
    gender      = random.choice(GENDERS)
    impressions, clicks, reach = _anomaly_metrics(impressions, clicks, reach)
    return {
        "platform":           "Facebook",
        "campaign_name":      _anomaly_campaign(random.choice(CAMPAIGN_PREFIXES["Facebook"]) + fake.bothify("??##")),
        "ad_group_name":      fake.bothify("AdSet_??####"),
        "ad_name":            fake.bothify("Ad_??####"),
        "reporting_date":     _anomaly_date_field(d),
        "age_group":          random.choice(AGE_GROUPS),
        "gender":             _anomaly_gender(gender),
        "amount_spent":       spend,
        "currency":           _anomaly_currency("USD"),
        "impressions":        impressions,
        "reach":              reach,
        "clicks":             clicks,
        "conversions":        random.randint(0, max(1, clicks // 5)),
        "video_plays_25pct":  plays_25,
        "video_plays_50pct":  plays_50,
        "video_plays_100pct": plays_100,
        "objective":          random.choice(["CONVERSIONS", "REACH", "BRAND_AWARENESS", "TRAFFIC"]),
        "ad_format":          random.choice(["Image", "Video", "Carousel", "Story"]),
    }

def _instagram_row() -> dict:
    impressions = random.randint(500, 300_000)
    reach       = int(impressions * random.uniform(0.55, 0.92))
    clicks      = random.randint(5, max(6, int(impressions * 0.04)))
    spend       = _anomaly_spend(round(random.uniform(5.0, 3_000.0), 2))
    plays_25    = int(impressions * random.uniform(0.15, 0.65))
    plays_50    = int(plays_25 * random.uniform(0.40, 0.80))
    plays_100   = int(plays_50 * random.uniform(0.25, 0.70))
    d           = _rand_date(START_DATE, END_DATE)
    gender      = random.choice(GENDERS)
    impressions, clicks, reach = _anomaly_metrics(impressions, clicks, reach)
    return {
        "platform":           "Instagram",
        "campaign_name":      _anomaly_campaign(random.choice(CAMPAIGN_PREFIXES["Instagram"]) + fake.bothify("??##")),
        "ad_group_name":      fake.bothify("IGAdSet_??####"),
        "ad_name":            fake.bothify("IGAd_??####"),
        "reporting_date":     _anomaly_date_field(d),
        "age_group":          random.choice(AGE_GROUPS),
        "gender":             _anomaly_gender(gender),
        "amount_spent":       spend,
        "currency":           _anomaly_currency("USD"),
        "impressions":        impressions,
        "reach":              reach,
        "clicks":             clicks,
        "conversions":        random.randint(0, max(1, clicks // 6)),
        "video_plays_25pct":  plays_25,
        "video_plays_50pct":  plays_50,
        "video_plays_100pct": plays_100,
        "placement":          random.choice(["Feed", "Reels", "Stories", "Explore"]),
        "ig_media_type":      random.choice(["IMAGE", "VIDEO", "CAROUSEL_ALBUM"]),
    }

def _youtube_row() -> dict:
    impressions = random.randint(2_000, 800_000)
    views       = int(impressions * random.uniform(0.05, 0.40))
    clicks      = random.randint(10, max(11, int(views * 0.08)))
    spend       = _anomaly_spend(round(random.uniform(10.0, 8_000.0), 2))
    plays_25    = int(views * random.uniform(0.50, 0.90))
    plays_50    = int(plays_25 * random.uniform(0.45, 0.85))
    plays_100   = int(plays_50 * random.uniform(0.30, 0.70))
    d           = _rand_date(START_DATE, END_DATE)
    gender      = random.choice(GENDERS)
    impressions, clicks, _ = _anomaly_metrics(impressions, clicks, 0)
    return {
        "platform":           "YouTube",
        "campaign_name":      _anomaly_campaign(random.choice(CAMPAIGN_PREFIXES["YouTube"]) + fake.bothify("??##")),
        "ad_group_name":      fake.bothify("YTAdGrp_??####"),
        "ad_name":            fake.bothify("YTAd_??####"),
        "reporting_date":     _anomaly_date_field(d),
        "age_group":          random.choice(AGE_GROUPS),
        "gender":             _anomaly_gender(gender),
        "cost":               spend,
        "currency":           _anomaly_currency("USD"),
        "impressions":        impressions,
        "views":              views,
        "clicks":             clicks,
        "conversions":        random.randint(0, max(1, clicks // 4)),
        "video_plays_25pct":  plays_25,
        "video_plays_50pct":  plays_50,
        "video_plays_100pct": plays_100,
        "ad_type":            random.choice(["TrueView In-Stream", "Bumper", "Non-skippable", "Discovery"]),
        "video_duration_sec": random.choice([6, 15, 30, 60, 90, 120]),
    }

def _google_ads_row() -> dict:
    impressions = random.randint(500, 200_000)
    clicks      = random.randint(5, max(6, int(impressions * 0.10)))
    spend_usd   = round(random.uniform(5.0, 10_000.0), 2)
    cost_micros = _anomaly_cost_micros(int(spend_usd * 1_000_000))
    d           = _rand_date(START_DATE, END_DATE)
    gender      = random.choice(GENDERS)
    impressions, clicks, _ = _anomaly_metrics(impressions, clicks, 0)
    return {
        "platform":                "Google Ads",
        "campaign_name":           _anomaly_campaign(random.choice(CAMPAIGN_PREFIXES["Google Ads"]) + fake.bothify("??##")),
        "ad_group_name":           fake.bothify("GGLAdGrp_??####"),
        "ad_name":                 fake.bothify("GGLAd_??####"),
        "reporting_date":          _anomaly_date_field(d),
        "age_group":               random.choice(AGE_GROUPS),
        "gender":                  _anomaly_gender(gender),
        "cost_micros":             cost_micros,
        "currency":                _anomaly_currency("USD"),
        "impressions":             impressions,
        "clicks":                  clicks,
        "conversions":             round(random.uniform(0, max(0.1, clicks * 0.15)), 2),
        "video_plays_25pct":       0,
        "video_plays_50pct":       0,
        "video_plays_100pct":      0,
        "search_impression_share": round(random.uniform(0.10, 0.95), 4),
        "quality_score":           random.randint(1, 10),
        "device":                  random.choice(["Mobile", "Desktop", "Tablet"]),
        "match_type":              random.choice(["BROAD", "PHRASE", "EXACT"]),
    }

PLATFORM_BUILDERS = {
    "facebook":   _facebook_row,
    "instagram":  _instagram_row,
    "youtube":    _youtube_row,
    "google_ads": _google_ads_row,
}

# ── Serialisers ────────────────────────────────────────────
def _to_csv_bytes(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

def _to_json_bytes(df: pd.DataFrame) -> bytes:
    records = df.to_dict(orient="records")
    return json.dumps(records, indent=2, default=str).encode("utf-8")

def _to_parquet_bytes(df: pd.DataFrame) -> bytes:
    df_safe = df.copy()
    for col in df_safe.select_dtypes(include="object").columns:
        df_safe[col] = df_safe[col].astype(str)
    buf = io.BytesIO()
    df_safe.to_parquet(buf, index=False, engine="pyarrow", compression="snappy")
    buf.seek(0)
    return buf.read()

def _to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="RawData")
        ws = writer.sheets["RawData"]
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 40)
    buf.seek(0)
    return buf.read()

FORMAT_CONFIG = {
    "csv":     (_to_csv_bytes,     ".csv",     "text/csv"),
    "json":    (_to_json_bytes,    ".json",    "application/json"),
    "parquet": (_to_parquet_bytes, ".parquet", "application/octet-stream"),
    "excel":   (_to_excel_bytes,   ".xlsx",    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
}

# ── S3 Upload ──────────────────────────────────────────────
def _upload_to_s3(s3_client, bucket: str, key: str, data: bytes, content_type: str):
    s3_client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    logger.info("Uploaded s3://%s/%s (%d bytes)", bucket, key, len(data))

# ── Lambda Handler ─────────────────────────────────────────
def lambda_handler(event: dict, context):
    if not S3_BUCKET:
        raise ValueError("S3_BUCKET environment variable is required.")

    num_records = int(event.get("num_records", NUM_RECORDS))
    run_date    = datetime.utcnow().strftime("%Y-%m-%d")
    s3_client   = boto3.client("s3")
    manifest    = []
    errors      = []

    logger.info("Starting data generation: bucket=%s prefix=%s records=%d", S3_BUCKET, S3_PREFIX, num_records)

    for slug, builder in PLATFORM_BUILDERS.items():
        rows = [builder() for _ in range(num_records)]
        df = pd.DataFrame(rows)

        for fmt, (serialiser, ext, content_type) in FORMAT_CONFIG.items():
            try:
                data = serialiser(df)
                s3_key = f"{S3_PREFIX}/{slug}/{run_date}/{slug}_raw{ext}"
                _upload_to_s3(s3_client, S3_BUCKET, s3_key, data, content_type)
                manifest.append({"platform": slug, "format": fmt, "s3_key": s3_key, "rows": len(df), "bytes": len(data)})
            except Exception as e:
                logger.error("Failed for %s/%s: %s", slug, fmt, e)
                errors.append(str(e))

    # Upload run manifest
    manifest_payload = {
        "run_date": run_date,
        "num_records_per_file": num_records,
        "files": manifest,
        "errors": errors,
    }
    manifest_key = f"{S3_PREFIX}/_manifests/{run_date}_run_manifest.json"
    try:
        _upload_to_s3(s3_client, S3_BUCKET, manifest_key, json.dumps(manifest_payload, indent=2).encode("utf-8"), "application/json")
    except Exception as e:
        logger.error("Failed to upload manifest: %s", e)

    return {
        "statusCode": 200 if not errors else 207,
        "files_written": len(manifest),
        "errors": errors,
        "manifest_s3": f"s3://{S3_BUCKET}/{manifest_key}",
        "files": manifest,
    }