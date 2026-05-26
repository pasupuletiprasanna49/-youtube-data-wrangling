import pandas as pd
import numpy as np
import re
import hashlib

# ─────────────────────────────────────────────
# STEP 1 — Load raw dataset
# ─────────────────────────────────────────────
df = pd.read_csv('youtube_recommendation_dataset -.csv')
print(f"Raw shape: {df.shape}")

# ─────────────────────────────────────────────
# STEP 2 — Drop always-zero column (favorite_count)
# ─────────────────────────────────────────────
df.drop(columns=['favorite_count'], inplace=True)

# ─────────────────────────────────────────────
# STEP 3 — Standardise published_at to datetime
# ─────────────────────────────────────────────
df['published_at'] = pd.to_datetime(df['published_at'], utc=True)

# ─────────────────────────────────────────────
# STEP 4 — Map category_id → human-readable name
# ─────────────────────────────────────────────
cat_map = {
    1: 'Film & Animation', 10: 'Music', 17: 'Sports',
    19: 'Travel & Events', 20: 'Gaming', 22: 'People & Blogs',
    23: 'Comedy', 24: 'Entertainment', 25: 'News & Politics',
    26: 'Howto & Style', 27: 'Education', 28: 'Science & Technology'
}
df['category_name'] = df['category_id'].map(cat_map).fillna('Unknown')

# ─────────────────────────────────────────────
# STEP 5 — Parse ISO 8601 duration → readable label
# ─────────────────────────────────────────────
def parse_duration_label(iso):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', str(iso))
    if not match:
        return 'Unknown'
    h, m, s = (int(x) if x else 0 for x in match.groups())
    total = h * 3600 + m * 60 + s
    if total < 60:
        return 'Short (< 1 min)'
    elif total <= 300:
        return 'Medium (1–5 min)'
    elif total <= 1200:
        return 'Long (5–20 min)'
    else:
        return 'Very Long (> 20 min)'

df['duration_label'] = df['duration'].apply(parse_duration_label)

# ─────────────────────────────────────────────
# STEP 6 — Standardise text columns
# ─────────────────────────────────────────────
df['definition'] = df['definition'].str.lower().str.strip()
df['Title'] = df['Title'].str.strip()
df['channel_title'] = df['channel_title'].str.strip()

# ─────────────────────────────────────────────
# STEP 7 — Flag view_count outliers (IQR method)
# ─────────────────────────────────────────────
Q1 = df['view_count'].quantile(0.25)
Q3 = df['view_count'].quantile(0.75)
IQR = Q3 - Q1
df['is_view_outlier'] = df['view_count'] > (Q3 + 1.5 * IQR)

# ─────────────────────────────────────────────
# STEP 8 — Flag zero-view videos
# ─────────────────────────────────────────────
df['has_zero_views'] = df['view_count'] == 0

# ─────────────────────────────────────────────
# STEP 9 — Handle near-duplicate titles
# (same title + same channel = likely re-upload; flag, keep all)
# ─────────────────────────────────────────────
df['is_title_duplicate'] = df.duplicated(subset=['Title', 'channel_title'], keep=False)

# ─────────────────────────────────────────────
# STEP 10 — Feature engineering
# ─────────────────────────────────────────────
# Views per day of age
df['views_per_day'] = (df['view_count'] / df['video_age_days'].replace(0, 1)).round(2)

# Engagement tier
def engagement_tier(r):
    if r >= 0.05: return 'High'
    elif r >= 0.02: return 'Medium'
    else: return 'Low'

df['engagement_tier'] = df['engagement_rate'].apply(engagement_tier)

# Is HD
df['is_hd'] = df['definition'] == 'hd'

# ─────────────────────────────────────────────
# STEP 11 — Reorder & save
# ─────────────────────────────────────────────
df.to_csv('youtube_cleaned.csv', index=False)
print(f"Cleaned shape: {df.shape}")
print(f"New columns added: duration_label, category_name, is_view_outlier, has_zero_views, is_title_duplicate, views_per_day, engagement_tier, is_hd")
print(f"\nColumn list:\n{df.columns.tolist()}")
print(f"\nSample row:\n{df.iloc[0].to_dict()}")
