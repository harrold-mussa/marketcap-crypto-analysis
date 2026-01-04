# Project Background

---

Using CoinMarketCap's API to get a list of crypto coins.

**Data Source**: CoinMarketCap API Key

**Storage**: Locally saved in /data/raw and /data/processed folders

**Processing**: Using the following:
- Python
- Pandas
- Docker for AWS Image
- DuckDB

## Star Schema Layout

They will be placed into the necessary tables that will be created. A star schema is created, with involves a fact table, and 3 dimension tables. 
Down below is the fact table called fact_crypto_prices:
1. fact_id
2. tag_key -> FK to dim_tags
3. coin_key -> FK to dim_coins
4. date_key -> FK to dim_date
5. price_usd
6. market_cap
7. volume_24h
8. percentage_change_24h

Down below is the 1st dimension table called dim_coins:
1. coin_key FROM fact_crypto_prices
2. symbol -> CHAR 3
3. name
4. slug
5. is_active BOOLEAN
6. category 

Down below is the 2nd dimension table called dim_date:
1. date_key FROM fact_crypto_prices
2. full_timestamp
3. hour
4. day_name 
5. month
6. is_market_holiday

Down below is the 3rd dimension table called dim_tags:
1. tag_key FROM fact_crypto_prices
2. tag_name
3. tag_slug
