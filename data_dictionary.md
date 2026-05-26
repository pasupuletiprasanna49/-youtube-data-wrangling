# Data Dictionary — YouTube Recommendation Dataset

**Dataset:** youtube_recommendation_dataset.csv  
**Source:** YouTube Data API  
**Rows:** 537 videos | **Original columns:** 16 | **After cleaning:** 23  
**Purpose:** Analyse patterns in YouTube video recommendations — engagement, category, duration, and virality signals.

---

## Original Columns

| Column | Type | Description | Business / Analysis Relevance |
|--------|------|-------------|-------------------------------|
| `Title` | string | Video title as shown on YouTube | Identify content themes; detect duplicates |
| `channel_title` | string | Name of the YouTube channel | Channel-level performance grouping |
| `published_at` | datetime (UTC) | Date and time the video was published | Time-series trends; recency analysis |
| `category_id` | integer | YouTube numeric category code (1–28) | Maps to `category_name` after cleaning |
| `view_count` | integer | Total views at time of data collection | Primary popularity metric |
| `like_count` | integer | Total likes on the video | Positive sentiment signal |
| `comment_count` | integer | Total comments | Community engagement indicator |
| `favorite_count` | integer | Favourites count — **always 0 in this dataset** | **Dropped** — no analytical value |
| `duration` | string | ISO 8601 format (e.g. PT1M51S = 1 min 51 sec) | Raw format; converted to `duration_label` |
| `definition` | string | Video quality: `hd` or `sd` | Production quality flag |
| `caption` | boolean | Whether captions/subtitles exist | Accessibility; SEO signal |
| `engagement_rate` | float | (likes + comments) / views | Overall interaction level |
| `likes_to_views_ratio` | float | likes / views | Like conversion rate |
| `comments_to_views_ratio` | float | comments / views | Comment conversion rate |
| `duration_seconds` | integer | Duration in seconds (numeric form of `duration`) | Used for sorting/filtering by length |
| `video_age_days` | integer | Days since the video was published | Normalises view counts for fair comparison |

---

## New Columns Added During Cleaning

| Column | Type | How It Was Created | Why It's Useful |
|--------|------|--------------------|-----------------|
| `category_name` | string | Mapped from `category_id` using YouTube's official category list | Human-readable; easier to filter and plot |
| `duration_label` | string | Parsed `duration` ISO string into 4 buckets: Short / Medium / Long / Very Long | Enables duration-segment analysis without manual thresholds |
| `is_view_outlier` | boolean | IQR method: True if view_count > Q3 + 1.5×IQR | Flag viral videos; exclude from average calculations if needed |
| `has_zero_views` | boolean | True if view_count == 0 | Identify newly uploaded or restricted videos |
| `is_title_duplicate` | boolean | True if same Title + channel_title appears more than once | Detects re-uploads or split videos |
| `views_per_day` | float | view_count / video_age_days (min 1 to avoid division by zero) | Fair comparison of old vs new videos |
| `engagement_tier` | string | Low (<2%), Medium (2–5%), High (≥5%) based on engagement_rate | Quick segmentation for dashboards and charts |
| `is_hd` | boolean | True if definition == 'hd' | Binary quality flag for modelling |

---

## Data Quality Summary

| Issue | Count | Action Taken |
|-------|-------|--------------|
| Missing values | 0 | None needed |
| Duplicate rows (exact) | 0 | None needed |
| Duplicate titles (same channel) | 7 rows / 3 title groups | Flagged with `is_title_duplicate`; kept all rows |
| Zero-view videos | 1 | Flagged with `has_zero_views` |
| View count outliers (IQR) | 62 | Flagged with `is_view_outlier`; not deleted |
| `favorite_count` always 0 | 537 | Column dropped |
| `published_at` timezone inconsistency | All rows | Standardised to UTC datetime |
| ISO 8601 duration strings | All rows | Parsed into `duration_label` categories |
| `category_id` numeric only | All rows | Mapped to `category_name` |

---

## Category ID Reference

| category_id | category_name |
|-------------|---------------|
| 1 | Film & Animation |
| 10 | Music |
| 17 | Sports |
| 19 | Travel & Events |
| 20 | Gaming |
| 22 | People & Blogs |
| 23 | Comedy |
| 24 | Entertainment |
| 25 | News & Politics |
| 26 | Howto & Style |
| 27 | Education |
| 28 | Science & Technology |
