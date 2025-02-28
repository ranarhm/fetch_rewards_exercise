**Entity Relationship Diagram**

+----------------+       +-------------------+       +----------------+
|     Users      |       |     Receipts      |       |     Brands     |
+----------------+       +-------------------+       +----------------+
| user_id (PK)   |<----->| receipt_id (PK)   |       | brand_id (PK)  |
| state          |       | user_id (FK)      |       | barcode        |
| created_date   |       | purchase_date     |       | brand_code     |
| last_login     |       | date_scanned      |       | name           |
| role           |       | finished_date     |       | category       |
| active         |       | points_earned     |       | category_code  |
+----------------+       | bonus_points      |       | top_brand      |
                         | bonus_reason      |       +----------------+
                         | total_spent       |               ^
                         | item_count        |               |
                         | status            |               |
                         +-------------------+               |
                                  |                          |
                                  |                          |
                                  v                          |
                         +-------------------+               |
                         | Receipt_Items     |               |
                         +-------------------+               |
                         | item_id (PK)      |               |
                         | receipt_id (FK)   |-----------------+
                         | brand_id (FK)     |
                         | quantity          |
                         | price             |
                         | points_earned     |
                         | description       |
                         +-------------------+


**Dimensional Data Model - Star Schema**

+----------------------+       +----------------------+
|     Dim_Users        |       |     Dim_Date         |
+----------------------+       +----------------------+
| user_key (PK)        |       | date_key (PK)        |
| user_id              |       | date                 |
| state                |       | year                 |
| created_date         |       | month                |
| last_login           |       | day                  |
| role                 |       | quarter              |
| active               |       | is_weekend           |
| user_age_days        |       +----------------------+
+----------------------+                ^
          ^                              |
          |                              |
          |                              |
+--------------------------+             |
|     Fact_Receipts        |-------------+
+--------------------------+
| receipt_key (PK)         |
| receipt_id               |
| user_key (FK)            |
| purchase_date_key (FK)   |
| scan_date_key (FK)       |
| total_spent              |
| item_count               |
| points_earned            |
| status                   |
+--------------------------+
          ^
          |
          |
+-------------------------+      +-------------------+
|   Fact_Receipt_Items    |      |   Dim_Brands      |
+-------------------------+      +-------------------+
| item_key (PK)           |      | brand_key (PK)    |
| receipt_key (FK)        |      | brand_id          |
| brand_key (FK)          |------| brand_code        |
| quantity                |      | name              |
| price                   |      | category          |
| points_earned           |      | category_code     |
| description             |      | top_brand         |
+-------------------------+      +-------------------+