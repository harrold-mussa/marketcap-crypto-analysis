import os
import boto3 

import pandas as pd

from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name = os.getenv("AWS_DEFAULT_REGION_ID"),
    endpoint_url = os.getenv("LOCALSTACK_ENDPOINT")
)

# Function to transform data from Silver to Gold layer down below:
def transform_silver_to_gold():
    bucket = os.getenv("S3_BUCKET")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix='silver/')

    if 'Contents' not in response:
        print("No objects found in the 'silver/' prefix.")
        return
    
    all_files_silver = sorted(response['Contents'], key=lambda x: x['LastModified'])
    latest_file_key_silver = all_files_silver[-1]['Key']
    print(f"Latest file to process: {latest_file_key_silver}")

    obj = s3_client.get_object(Bucket=bucket, Key=latest_file_key_silver)
    df = pd.read_parquet(BytesIO(obj['Body'].read()))

    dim_coins = df[['ticker', 'coin_name']].drop_duplicates().reset_index(drop=True)
    dim_coins['coin_id'] = dim_coins.index + 1

    df['api_timestamp'] = pd.to_datetime(df['api_timestamp'])

    dim_date = pd.DataFrame({
        'full_timestamp': df['api_timestamp'],
        'year': df['api_timestamp'].dt.year,
        'month': df['api_timestamp'].dt.month,
        'day': df['api_timestamp'].dt.day,
        'hour': df['api_timestamp'].dt.hour
    })
    dim_date['date_id'] = dim_date['full_timestamp'].dt.strftime('%Y%m%d%H')
    dim_date = dim_date.drop_duplicates().reset_index(drop=True)

    fact_listings = df.merge(dim_coins, on=['ticker', 'coin_name'])
    fact_listings['date_id'] = fact_listings['api_timestamp'].dt.strftime('%Y%m%d%H')
    fact_listings = fact_listings[['coin_id', 'date_id', 'price_usd', 'market_cap', 'rank']]

    tables = {
        'dim_coins': dim_coins,
        'dim_date': dim_date,
        'fact_listings': fact_listings
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for name, table_df in tables.items():
        buffer = BytesIO()
        table_df.to_parquet(buffer, index=False)

        gold_key = f"gold/{name}_{timestamp}.parquet"

        s3_client.put_object(
            Bucket=bucket,
            Key=gold_key,
            Body=buffer.getvalue()
        )
        print(f"Transformed data saved to: {gold_key}")

# Running the transformation function down here:
if __name__ == "__main__":
    transform_silver_to_gold()