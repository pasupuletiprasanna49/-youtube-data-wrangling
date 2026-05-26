#  YouTube Data Wrangling — Data Immersion Assignment

##  Objective
Clean and prepare a raw YouTube Recommendation Dataset for analysis
by identifying data quality issues and resolving them using Python.

##  Dataset
- **Source:** YouTube Data API v3
- **Raw shape:** 537 rows × 16 columns
- **Cleaned shape:** 537 rows × 23 columns

##  Data Quality Issues Found
| Issue | Details |
|-------|---------|
| Duplicate videos | 4 videos appeared 2–3 times |
| Unreadable categories | category_id was a number (e.g. 27) not a name |
| Unreadable duration | Stored as PT3M25S instead of human-readable format |
| Useless column | favorite_count was 0 for all 537 rows (deprecated by YouTube) |
| View count outliers | 62 videos with unusually high views flagged |
| Zero views row | 1 video had 0 views — likely a data error |
| Likes showing zero | 12 videos with 0 likes — likes may be disabled |

##  What Was Done
- Removed duplicate video entries
- Mapped numeric category IDs to readable names (Education, Music, Gaming...)
- Converted ISO duration strings to human-readable buckets
- Dropped the deprecated favorite_count column
- Flagged outliers and anomalies without deleting them
- Feature engineered 7 new meaningful columns

##  New Columns Added
| Column | Description |
|--------|-------------|
| category_name | Human-readable category (e.g. Education) |
| duration_label | Short / Medium / Long / Very Long |
| is_view_outlier | True if video has unusually high views |
| has_zero_views | True if view_count is 0 |
| is_title_duplicate | True if same title appears multiple times |
| views_per_day | view_count divided by video_age_days |
| engagement_tier | High / Medium / Low engagement label |
| is_hd | True if video is HD quality |

##  Files
| File | Description |
|------|-------------|
| cleaning_script.py | Python script to clean the dataset |
| data_dictionary.md | Explanation of all 23 columns |
| youtube_cleaned.csv | Final cleaned dataset |
| youtube_recommendation_dataset-.csv | Original raw dataset |

## How to Run
pip install pandas numpy
python cleaning_script.py

## 🛠️ Tools Used
- Python 3.13
- Pandas
- NumPy
- VS Code
