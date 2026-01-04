# Project Background

<img>

## Overview

Using CoinMarketCap's API, I built an automated pipeline that extracts cryptocoins and its details by calling the API, saving them into JSON files, viewed in the `data/raw` folder. They are then transformed and saved as a parquet, viewed in the `data/processed` folder. Percentage changes and volumes within 24 hours moving ranges are calculated onto a dashboard.

```mermaid
graph LR
    subgraph "Local Computer"
        A[CoinMarketCap API] -- "Python Requests" --> DOCKER

        subgraph DOCKER [Docker Container: LocalStack]
            direction TB
            S3_RAW[(S3 Bucket: /raw)] 
            LAMBDA[Lambda: Ingestion]
            GLUE[Glue: ETL Job]
            S3_GOLD[(S3 Bucket: /gold)]
            
            LAMBDA --> S3_RAW
            S3_RAW --> GLUE
            GLUE --> S3_GOLD
        end

        subgraph "Star Schema Modeling"
            S3_GOLD --> DIM_C[dim_coins]
            S3_GOLD --> DIM_D[dim_date]
            S3_GOLD --> FACT[fact_listings]
        end

        S3_GOLD -- "SQL Query" --> ATHENA[Athena / DuckDB]
        ATHENA --> BI[Power BI / Dashboard]
    end

    style DOCKER fill:#f5f5f5,stroke:#232f3e,stroke-width:2px,stroke-dasharray: 5 5
    style S3_RAW fill:#ff9900,color:#fff
    style S3_GOLD fill:#ff9900,color:#fff
    style LAMBDA fill:#ec7211,color:#fff
    style GLUE fill:#ec7211,color:#fff
```
