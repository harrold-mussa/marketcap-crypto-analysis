import os 
import json
import requests
import boto3

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
# Loading the .env CryptoMarketCap API Key down here:
cmc_api_key = os.getenv("CMC_API_KEY")
# Loading the .env LocalStack Endpoint Key down here:
endpoint_key = os.getenv("LOCALSTACK_ENDPOINT")
print(f"Loaded for endpoint: {endpoint_key}")
# Loading the .env S3 Bucket down here:
s3_bucket = os.getenv("S3_BUCKET")
# Loading the .env AWS details down here:
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_default_region_id = os.getenv("AWS_DEFAULT_REGION_ID")
# Initializing S3 Client using boto3 down here:
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_default_region_id,
    endpoint_url=endpoint_key
)

# Fetching API from CoinMarketCap and following its API Documentation, view down below:
def fetching_api():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD',
        'sort': 'market_cap',
        'aux': 'cmc_rank,tags,platform,total_supply,max_supply'
    }
    # Following the CoinMarketCap's API Documentation of using Session down below:
    with requests.Session() as session:
        session.headers.update({
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': cmc_api_key
        })

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(f"Network Error occured: {e}")
            return None
        
# Saving data to S3 Bronze Layer Bucket, view down below:    
def save_to_s3_bronze(data):
    if not data:
        print("No data to save to S3.")
        return
    
    s3_bucket_name = os.getenv("S3_BUCKET")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    partition_path = now.strftime("year=%Y/month=%m/day=%d/")
    file_key = f"bronze/{partition_path}/cmc_raw_{timestamp}.json"

    try:
        s3_client.put_object(
        Bucket=s3_bucket_name,
        Key=file_key,
        Body=json.dumps(data)
        )
        print(f"Data successfully saved to S3 to: {file_key}")
    except Exception as e:
        print(f"Failed to load data to S3: {e}")
    
if __name__ == "__main__":
    cmc_data = fetching_api()
    if cmc_data:
        save_to_s3_bronze(cmc_data)
    else:
        print("Error in fetching data. Skipping S3 upload")



