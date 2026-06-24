-- ============================================================
-- Unity Catalog Setup - Retail Streaming Lakehouse
-- ============================================================

-- ============================================================
-- 1. CATALOG & SCHEMAS
-- ============================================================
CREATE CATALOG IF NOT EXISTS retail_lakehouse
  COMMENT 'Retail streaming lakehouse - dev and prod environments';

CREATE SCHEMA IF NOT EXISTS retail_lakehouse.dev
  COMMENT 'Development environment';

CREATE SCHEMA IF NOT EXISTS retail_lakehouse.prod
  COMMENT 'Production environment';

-- ============================================================
-- 2. ROW LEVEL SECURITY - store_id based access
-- Each user can only see rows matching their assigned store
-- Admins see all rows
-- ============================================================
CREATE ROW FILTER IF NOT EXISTS retail_lakehouse.dev.store_row_filter
ON retail_lakehouse.dev.silver_orders (store_id STRING)
RETURN is_account_group_member('admins')
    OR store_id = current_user();

ALTER TABLE retail_lakehouse.dev.silver_orders
  SET ROW FILTER retail_lakehouse.dev.store_row_filter ON (store_id);

-- prod
CREATE ROW FILTER IF NOT EXISTS retail_lakehouse.prod.store_row_filter
ON retail_lakehouse.prod.silver_orders (store_id STRING)
RETURN is_account_group_member('admins')
    OR store_id = current_user();

ALTER TABLE retail_lakehouse.prod.silver_orders
  SET ROW FILTER retail_lakehouse.prod.store_row_filter ON (store_id);

-- ============================================================
-- 3. COLUMN MASKING - email and phone for non-admins
-- ============================================================
CREATE MASKING POLICY IF NOT EXISTS retail_lakehouse.dev.mask_email
AS (email STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN email
  ELSE regexp_replace(email, '^[^@]+', '***')
END;

CREATE MASKING POLICY IF NOT EXISTS retail_lakehouse.dev.mask_phone
AS (phone STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN phone
  ELSE regexp_replace(phone, '.', '*', 1, char_length(phone) - 2)
END;

ALTER TABLE retail_lakehouse.dev.silver_orders
  ALTER COLUMN customer_email
  SET MASKING POLICY retail_lakehouse.dev.mask_email;

ALTER TABLE retail_lakehouse.dev.silver_orders
  ALTER COLUMN customer_phone
  SET MASKING POLICY retail_lakehouse.dev.mask_phone;

-- prod
CREATE MASKING POLICY IF NOT EXISTS retail_lakehouse.prod.mask_email
AS (email STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN email
  ELSE regexp_replace(email, '^[^@]+', '***')
END;

CREATE MASKING POLICY IF NOT EXISTS retail_lakehouse.prod.mask_phone
AS (phone STRING) RETURNS STRING
RETURN CASE
  WHEN is_account_group_member('admins') THEN phone
  ELSE regexp_replace(phone, '.', '*', 1, char_length(phone) - 2)
END;

ALTER TABLE retail_lakehouse.prod.silver_orders
  ALTER COLUMN customer_email
  SET MASKING POLICY retail_lakehouse.prod.mask_email;

ALTER TABLE retail_lakehouse.prod.silver_orders
  ALTER COLUMN customer_phone
  SET MASKING POLICY retail_lakehouse.prod.mask_phone;

-- ============================================================
-- 4. GRANTS
-- ============================================================
GRANT USE CATALOG ON CATALOG retail_lakehouse TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA retail_lakehouse.dev TO `data_engineers`;
GRANT USE SCHEMA ON SCHEMA retail_lakehouse.prod TO `data_engineers`;
GRANT SELECT ON SCHEMA retail_lakehouse.dev TO `data_engineers`;
GRANT SELECT ON SCHEMA retail_lakehouse.prod TO `data_engineers`;