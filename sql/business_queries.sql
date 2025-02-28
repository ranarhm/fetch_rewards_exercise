-- Query 1: What are the top 5 brands by receipts scanned for most recent month?
WITH recent_month AS (
    SELECT 
        MAX(DATE_TRUNC('month', r.purchase_date)) AS month
    FROM 
        fact_receipts r
)

SELECT 
    b.name AS brand_name,
    COUNT(DISTINCT ri.receipt_key) AS receipt_count
FROM 
    fact_receipt_items ri
JOIN 
    dim_brands b ON ri.brand_key = b.brand_key
JOIN 
    fact_receipts r ON ri.receipt_key = r.receipt_key
JOIN 
    recent_month rm ON DATE_TRUNC('month', r.purchase_date) = rm.month
GROUP BY 
    b.name
ORDER BY 
    receipt_count DESC
LIMIT 5;


-- Query 2: When considering average spend from receipts with 'rewardsReceiptStatus' of 'Accepted' or 'Rejected', which is greater?
SELECT 
    r.status,
    AVG(r.total_spent) AS average_spend
FROM 
    fact_receipts r
WHERE 
    r.status IN ('ACCEPTED', 'REJECTED')
GROUP BY 
    r.status
ORDER BY 
    average_spend DESC;


-- Query 3: Which brand has the most spend among users who were created within the past 6 months?
SELECT 
    b.name AS brand_name,
    SUM(ri.price * ri.quantity) AS total_spend
FROM 
    fact_receipt_items ri
JOIN 
    fact_receipts r ON ri.receipt_key = r.receipt_key
JOIN 
    dim_brands b ON ri.brand_key = b.brand_key
JOIN 
    dim_users u ON r.user_key = u.user_key
WHERE 
    u.created_date >= (CURRENT_DATE - INTERVAL '6 months')
GROUP BY 
    b.name
ORDER BY 
    total_spend DESC
LIMIT 1;
