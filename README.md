# Project Background

<img>

## Overview

Using CoinMarketCap's API, I built an automated pipeline that extracts cryptocoins and its details by calling the API, saving them into JSON files, viewed in the `data/raw` folder. They are then transformed and saved as a parquet, viewed in the `data/processed` folder. Percentage changes and volumes within 24 hours moving ranges are calculated onto a dashboard.

```mermaid
graph LR
    %% Source
    API[CoinMarketCap API]

    subgraph "Ingestion Layer (Bronze)"
        Lambda[Python Ingestion Script / Lambda]
        S3_RAW[(S3 Bucket: /raw)]
    end

    subgraph "Transformation Layer (Silver)"
        Glue[Python ETL Script / Glue]
        S3_PROCESSED[(S3 Bucket: /processed)]
    end

    subgraph "Analytics Layer (Gold)"
        Modeling[Star Schema Modeling]
        S3_GOLD[(S3 Bucket: /gold)]
        DIM_C[dim_coins]
        DIM_D[dim_date]
        FACT[fact_listings]
    end

    %% Flow
    API -->|JSON| Lambda
    Lambda --> S3_RAW
    S3_RAW -->|Transform| Glue
    Glue --> S3_PROCESSED
    S3_PROCESSED --> Modeling
    Modeling --> S3_GOLD
    S3_GOLD --> DIM_C
    S3_GOLD --> DIM_D
    S3_GOLD --> FACT

    %% Final Consumption
    FACT --> ATHENA[Athena / DuckDB]
    ATHENA --> BI[Power BI Dashboard]

    %% Styling
    style S3_RAW fill:#f96,stroke:#333
    style S3_PROCESSED fill:#f96,stroke:#333
    style S3_GOLD fill:#f96,stroke:#333
    style API fill:#4CAF50,color:#fff
    style BI fill:#2196F3,color:#fff
```
