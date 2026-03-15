SELECT 
    MIN(latitude) AS min_lat_site, 
    MAX(latitude) AS max_lat_site,
    MIN(longitude) AS min_lon_site, 
    MAX(longitude) AS max_lon_site
FROM locations