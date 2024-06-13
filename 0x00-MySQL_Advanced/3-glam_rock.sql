-- This script  lists all bands with Glam rock as their main style, 
-- ranked by their longevity
ALTER TABLE metal_bands
ADD COLUMN lifespan INT;

UPDATE metal_bands
SET lifespan =	IF(split IS NULL, 2022 - formed, split - formed);

SELECT band_name, lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
