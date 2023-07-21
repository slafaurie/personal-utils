# Taken from https://jdlm.info/articles/2023/06/11/bootstrap-confidence-intervals-sql-postgresql-bigquery.html


WITH bootstrap_indexes AS (
  SELECT *
  FROM UNNEST(GENERATE_ARRAY(1,1000)) AS bootstrap_index
)

, bootstrap_data AS (
  SELECT  
  entity_id
  , city_id
  , city_name 
  , cluster_type
  , cluster_id 
  , n_indexes
  , h3.*
  , ROW_NUMBER() OVER(PARTITION BY entity_id, city_id, cluster_id ORDER BY h3_index) AS h3_idx
  FROM `logistics-data-storage-staging.long_term_pricing.sl_cusloc_clean_clusters` 
  LEFT JOIN UNNEST(indexes) h3
  WHERE entity_id = "FP_SG"
  and cluster_id = "High__1"
)


, bootstrap_map AS (
  SELECT bootstrap_index
  , entity_id
  , city_id
  , cluster_id
  , FLOOR(RAND() * n_indexes) as data_index
  FROM bootstrap_data bd
  CROSS JOIN bootstrap_indexes bi

)

, bootstrap AS (
  SELECT
  bootstrap_index
  , bm.entity_id
  , bm.city_id
  , bm.cluster_id
  , AVG(coef) as coef_avg
  FROM bootstrap_map bm
  INNER JOIN bootstrap_data bd
    ON bm.data_index = bd.h3_idx
    AND bm.entity_id = bd.entity_id
    AND bm.city_id = bd.city_id
    AND bm.cluster_id = bd.cluster_id
  GROUP BY 1,2,3,4
) 


, bootstrap_ci AS (
  SELECT 
  entity_id
  , city_id
  , cluster_id
  , AVG(coef_avg) as coef_avg
  , APPROX_QUANTILES(coef_avg, 1000)[OFFSET(25)] as coef_low
  , APPROX_QUANTILES(coef_avg, 1000)[OFFSET(975)] AS coef_high
  FROM bootstrap
  GROUP BY 1,2,3
)

SELECT *
FROM bootstrap_ci
