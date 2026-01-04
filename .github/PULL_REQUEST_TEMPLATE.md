## 🚀 Overview
*Briefly describe the changes. What part of the pipeline are we touching (Ingestion, Transform, or Load)?*

## 🛠 Type of Change
- [ ] 🏗️ **Infrastructure** (Docker, LocalStack config, S3 Buckets)
- [ ] 🐍 **Python Logic** (API calls, data cleaning)
- [ ] 📉 **Data Modeling** (Star Schema, dim/fact table changes)
- [ ] 🧪 **Testing/Quality** (Added data validation checks)

## 📊 Star Schema Impacts
*How does this affect our tables?*
- **New Tables:** (e.g., `dim_tags`)
- **Schema Changes:** (e.g., added `volume_24h` to `fact_listings`)

## 🧪 How I Tested This (LocalStack)
- [ ] `docker-compose up` runs without errors.
- [ ] Verified S3 data: `awslocal s3 ls s3://raw-data/`
- [ ] Verified Parquet files via DuckDB/Athena.
- [ ] (Optional) Attached a screenshot of the data preview.

## 📸 Screenshots / Data Preview
| Table Name | Row Count | Sample Data Preview |
| :--- | :--- | :--- |
| `fact_listings` | 100 | [Insert screenshot or table snippet] |

## 🔗 Related Issues
Fixes # (issue number)