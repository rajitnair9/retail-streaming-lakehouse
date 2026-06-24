-- ============================================================
-- Unity Catalog Setup - Retail Streaming Lakehouse
-- ============================================================

-- ============================================================
-- 1. CATALOGS
-- ============================================================
CREATE CATALOG IF NOT EXISTS dev_retail_lakehouse
  COMMENT 'Development environment - Retail Streaming Lakehouse';

CREATE CATALOG IF NOT EXISTS prod_retail_lakehouse
  COMMENT 'Production environment - Retail Streaming Lakehouse';

-- ============================================================
-- 2. SCHEMAS
-- ============================================================
CREATE SCHEMA IF NOT EXISTS dev_retail_lakehouse.retail
  COMMENT 'Retail domain - dev';

CREATE SCHEMA IF NOT EXISTS prod_retail_lakehouse.retail
  COMMENT 'Retail domain - prod';

-- ============================================================
-- 3. ROW LEVEL SECURITY
-- ============================================================

-- dev
CREATE ROW FILTER IF NOT EXISTS dev_retail_lakehouse.retail.store_row_filter
ON dev_retail_lakehouse.retail.silver_orders (store_id STRING)
RETURN is_account_group_member('admins')
    OR store_id = current_user();

ALTER TABLE dev_retail_lakehouse.retail.silver_orders
  SET ROW FILTER dev_retail_lakehouse.retail.store_row_filter ON (store_id);

-- prod
CREATE ROW FILTER IF NOT EXISTS prod_retail_lakehouse.retail.store_row_filter
ON prod_retail_lakehouse.retail.silver_orders (store_id STRING)
RETURN is_account_group_member('admins')
    OR store_id = current_user();

ALTER TABLE prod_retail_lakehouse.retail.silver_orders
  SET ROW FILTER prod_retail_lakehouse.retail.store_row_filter ON (store_id);

-- ============================================================
-- 4. COLUMN MASKING
-- ============================================================

-- dev
CREATE MASKING POLICY IF NOT EXISTS dev_retail_lakehouse.retail.mask_email
AS (email STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN email
  ELSE regexp_replace(email, '^[^@]+', '***')
END;

CREATE MASKING POLICY IF NOT EXISTS dev_retail_lakehouse.retail.mask_phone
AS (phone STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN phone
  ELSE regexp_replace(phone, '.', '*', 1, char_length(phone) - 2)
END;

ALTER TABLE dev_retail_lakehouse.retail.silver_orders
  ALTER COLUMN customer_email
  SET MASKING POLICY dev_retail_lakehouse.retail.mask_email;

ALTER TABLE dev_retail_lakehouse.retail.silver_orders
  ALTER COLUMN customer_phone
  SET MASKING POLICY dev_retail_lakehouse.retail.mask_phone;

-- prod
CREATE MASKING POLICY IF NOT EXISTS prod_retail_lakehouse.retail.mask_email
AS (email STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN email
  ELSE regexp_replace(email, '^[^@]+', '***')
END;

CREATE MASKING POLICY IF NOT EXISTS prod_retail_lakehouse.retail.mask_phone
AS (phone STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN phone
  ELSE regexp_replace(phone, '.', '*', 1, char_length(phone) - 2)
END;

ALTER TABLE prod_retail_lakehouse.retail.silver_orders
  ALTER COLUMN customer_email
  SET MASKING POLICY prod_retail_lakehouse.retail.mask_email;

ALTER TABLE prod_retail_lakehouse.retail.silver_orders
  ALTER COLUMN customer_phone
  SET MASKING POLICY prod_retail_lakehouse.retail.mask_phone;

-- ============================================================
-- 5. GRANTS
-- ============================================================

-- dev - engineers get full access
GRANT USE CATALOG ON CATALOG dev_retail_lakehouse TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA dev_retail_lakehouse.retail TO `data_engineers`;
GRANT SELECT, MODIFY ON SCHEMA dev_retail_lakehouse.retail TO `data_engineers`;

-- prod - engineers read only, analysts read only
GRANT USE CATALOG ON CATALOG prod_retail_lakehouse TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA prod_retail_lakehouse.retail TO `data_engineers`;
GRANT SELECT ON SCHEMA prod_retail_lakehouse.retail TO `data_engineers`;

GRANT USE CATALOG ON CATALOG prod_retail_lakehouse TO `analysts`;
GRANT USE SCHEMA ON SCHEMA prod_retail_lakehouse.retail TO `analysts`;
GRANT SELECT ON SCHEMA prod_retail_lakehouse.retail TO `analysts`;