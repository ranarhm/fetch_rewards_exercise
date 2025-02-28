import json
import pandas as pd
import gzip
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Load the data
def load_json_gz(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    return pd.DataFrame(data)

receipts_df = load_json_gz('receipts.json.gz')
users_df = load_json_gz('users.json.gz')
brands_df = load_json_gz('brands.json.gz')

# Data quality checks for receipts data
print("=== RECEIPTS DATA QUALITY ISSUES ===")
print(f"Total receipts: {len(receipts_df)}")
print(f"Duplicate receipts: {receipts_df['_id'].duplicated().sum()}")
print(f"Missing purchase dates: {receipts_df['purchaseDate'].isnull().sum()}")
print(f"Missing user IDs: {receipts_df['userId'].isnull().sum()}")
print(f"Missing total spent: {receipts_df['totalSpent'].isnull().sum()}")

# Check for inconsistent date formats and invalid dates
def check_date_field(df, field_name):
    issues = 0
    valid_dates = 0
    invalid_formats = 0
    
    if field_name not in df.columns:
        print(f"Field {field_name} not found")
        return
    
    for date in df[field_name].dropna():
        try:
            # Try to parse the date
            pd.to_datetime(date)
            valid_dates += 1
        except:
            invalid_formats += 1
    
    print(f"Field {field_name}: Valid dates: {valid_dates}, Invalid formats: {invalid_formats}")

date_fields = ['createDate', 'dateScanned', 'finishedDate', 'modifyDate', 'pointsAwardedDate', 'purchaseDate']
for field in date_fields:
    check_date_field(receipts_df, field)

# Check for negative values in numerical fields
for field in ['bonusPointsEarned', 'pointsEarned', 'purchasedItemCount', 'totalSpent']:
    if field in receipts_df.columns:
        neg_count = sum(receipts_df[field] < 0)
        print(f"Negative values in {field}: {neg_count}")

# Check receipt status distribution
status_counts = receipts_df['rewardsReceiptStatus'].value_counts()
print("\nReceipt Status Distribution:")
print(status_counts)

# Check for receipts with items but no total spent
if 'rewardsReceiptItemList' in receipts_df.columns:
    items_no_total = sum((receipts_df['rewardsReceiptItemList'].str.len() > 0) & 
                         (receipts_df['totalSpent'].isnull()))
    print(f"\nReceipts with items but no total spent: {items_no_total}")

# Data quality checks for users data
print("\n=== USERS DATA QUALITY ISSUES ===")
print(f"Total users: {len(users_df)}")
print(f"Duplicate user IDs: {users_df['_id'].duplicated().sum()}")
print(f"Missing state: {users_df['state'].isnull().sum()}")
print(f"Missing created date: {users_df['createdDate'].isnull().sum()}")

# Check state values
if 'state' in users_df.columns:
    invalid_states = sum(~users_df['state'].isin(list('ABCDEFGHIJKLMNOPQRSTUVWXY') + ['']))
    print(f"Invalid state values: {invalid_states}")

# Check for inactive users
if 'active' in users_df.columns:
    inactive_users = sum(~users_df['active'])
    print(f"Inactive users: {inactive_users}")

# Data quality checks for brands data
print("\n=== BRANDS DATA QUALITY ISSUES ===")
print(f"Total brands: {len(brands_df)}")
print(f"Duplicate brand IDs: {brands_df['_id'].duplicated().sum()}")
print(f"Missing brand names: {brands_df['name'].isnull().sum()}")

# Check for brands with multiple categories
if 'category' in brands_df.columns and 'name' in brands_df.columns:
    brands_with_multiple_categories = brands_df.groupby('name')['category'].nunique()
    multi_cat_brands = sum(brands_with_multiple_categories > 1)
    if multi_cat_brands > 0:
        print(f"\nBrands with multiple categories: {multi_cat_brands}")
        print(brands_with_multiple_categories[brands_with_multiple_categories > 1])

# Relationship checks
if 'userId' in receipts_df.columns and '_id' in users_df.columns:
    users_in_receipts = set(receipts_df['userId'].dropna())
    users_in_users = set(users_df['_id'].dropna())
    orphaned_receipts = len(users_in_receipts - users_in_users)
    print(f"\nReceipts with users not in users table: {orphaned_receipts}")

# Check for data distribution issues
print("\n=== DATA DISTRIBUTION ANALYSIS ===")

# Check total spent distribution
if 'totalSpent' in receipts_df.columns:
    spent_stats = receipts_df['totalSpent'].describe()
    print("\nTotal Spent Distribution:")
    print(spent_stats)
    
    # Check for outliers (more than 3 std devs from mean)
    mean = receipts_df['totalSpent'].mean()
    std = receipts_df['totalSpent'].std()
    outliers = sum((receipts_df['totalSpent'] > mean + 3*std) | 
                  (receipts_df['totalSpent'] < mean - 3*std))
    print(f"Potential outliers in total spent: {outliers}")