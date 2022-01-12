 -- pcts
 SELECT avg(n_viol)/365.0 as avg_viol_per_day, 
 percentile_cont(0.25) within group (order by n_viol/365.0 asc) as percentile_25,
 percentile_cont(0.50) within group (order by n_viol/365.0 asc) as percentile_50,
 percentile_cont(0.75) within group (order by n_viol/365.0 asc) as percentile_75,
 percentile_cont(0.95) within group (order by n_viol/365.0 asc) as percentile_95,
 percentile_cont(0.99) within group (order by n_viol/365.0 asc) as percentile_99,
 percentile_cont(0.999) within group (order by n_viol/365.0 asc) as percentile_999
 FROM (
 SELECT date_part('year', violationdate) as year, opa_account_num,  count(*) as n_viol
 FROM opa_properties_public opa
 LEFT JOIN violations vio
 ON opa.parcel_number = vio.opa_account_num
 GROUP BY opa_account_num, year, violationstatus, caseprioritydesc
 ) av
 WHERE year is not null
-- 2022-01-01
-- [{'avg_viol_per_day': 0.0072561207090027745,
--  'percentile_25': 0.0027397260273972603,
--  'percentile_50': 0.005479452054794521,
--  'percentile_75': 0.00821917808219178,
--  'percentile_95': 0.019178082191780823,
--  'percentile_99': 0.03287671232876712,
--  'percentile_999': 0.06027397260273973}]
