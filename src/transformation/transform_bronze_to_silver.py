import os
import json
import boto3

import pandas as pd

from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime 

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION_ID"),
    endpoint_url=os.getenv("LOCALSTACK_ENDPOINT") 
)

def transform_bronze_to_silver():
    bucket = os.getenv("S3_BUCKET")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix='bronze/')

    if 'Contents' not in response:
        print("No objects found in the 'bronze/' prefix.")
        return

    all_files = sorted(response['Contents'], key=lambda x: x['LastModified'])
    latest_file_key = all_files[-1]['Key']
    print(f"Latest file to process: {latest_file_key}")

    obj = s3_client.get_object(Bucket=bucket, Key=latest_file_key)
    raw_data = json.loads(obj['Body'].read().decode('utf-8'))
    df = pd.json_normalize(raw_data['data'])

    keep_cols = {
        'name': 'coin_name',
        'symbol': 'ticker',
        'cmc_rank': 'rank',
        'quote.USD.price': 'price_usd',
        'quote.USD.market_cap': 'market_cap',
        'last_updated': 'api_timestamp'
    }

    cleaned_df = df[keep_cols.keys()].rename(columns=keep_cols)
    cleaned_df['ingested_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    parquet_buffer = BytesIO()
    cleaned_df.to_parquet(parquet_buffer, index=False)

    silver_key = latest_file_key.replace('bronze/', 'silver/').replace('.json', '.parquet')
    s3_client.put_object(
        Bucket=bucket,
        Key=silver_key,
        Body=parquet_buffer.getvalue()
    )
    print(f"Transformed data saved to: {silver_key}")

if __name__ == "__main__": 
    transform_bronze_to_silver()