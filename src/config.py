from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Sales Analytics Dashboard"

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
]

OPTIONAL_COLUMNS = [
    "sales",
    "customer_id",
]

NUMERIC_COLUMNS = [
    "quantity",
    "unit_price",
    "sales",
]

TEXT_COLUMNS = [
    "order_id",
    "product",
    "category",
    "region",
    "customer_id",
]

DATE_COLUMNS = [
    "order_date",
]

COLUMN_ALIASES = {
    "order": "order_id",
    "orderid": "order_id",
    "order_no": "order_id",
    "order_number": "order_id",
    "orderdate": "order_date",
    "date": "order_date",
    "order_dt": "order_date",
    "item": "product",
    "product_name": "product",
    "productname": "product",
    "cat": "category",
    "category_name": "category",
    "location": "region",
    "area": "region",
    "region_name": "region",
    "qty": "quantity",
    "quantity_sold": "quantity",
    "units": "quantity",
    "price": "unit_price",
    "unitprice": "unit_price",
    "rate": "unit_price",
    "amount": "sales",
    "total": "sales",
    "total_sales": "sales",
    "sales_amount": "sales",
    "revenue": "sales",
    "customer": "customer_id",
    "cust_id": "customer_id",
    "customerid": "customer_id",
}

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_SAMPLE_PATH = BASE_DIR / "data" / "raw" / "sample_sales.csv"
PROCESSED_SAMPLE_PATH = BASE_DIR / "data" / "processed" / "cleaned_sales.csv"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

CURRENCY_SYMBOL = "$"

MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "15")) * 1024 * 1024