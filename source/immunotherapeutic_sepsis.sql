WITH immunotherapy_list AS (
    -- Define the comprehensive list of target drugs
    SELECT UNNEST(ARRAY[
        'pembrolizumab', 'keytruda', 'nivolumab', 'opdivo',
        'atezolizumab', 'tecentriq', 'durvalumab', 'imfinzi',
        'avelumab', 'bavencio', 'cemiplimab', 'libtayo',
        'dostarlimab', 'jemperli', 'tislelizumab', 'tevimbra',
        'toripalimab', 'loqtorzi', 'ipilimumab', 'yervoy',
        'tremelimumab', 'imjudo', 'relatlimab', 'opdualag'
    ]) AS drug_name
),
ed_immuno_patients AS (
    -- Identify ED stays where these drugs were mentioned in MedRecon
    SELECT DISTINCT 
        mr.stay_id, 
        mr.subject_id,
        mr.name AS matched_drug_name
    FROM mimiciv_ed.medrecon mr
    JOIN immunotherapy_list il 
      ON mr.name ILIKE '%' || il.drug_name || '%'
)
SELECT 
    s3.subject_id,
    s3.stay_id,
    s3.sofa_score,
    s3.suspected_infection_time,
    eip.matched_drug_name,
    ed.intime AS ed_arrival,
    -- Calculating time from arrival to suspected infection
    (s3.suspected_infection_time - ed.intime) AS time_to_infection
FROM mimiciv_derived.sepsis3 s3
INNER JOIN ed_immuno_patients eip 
    ON s3.stay_id = eip.stay_id
INNER JOIN mimiciv_ed.edstays ed 
    ON s3.stay_id = ed.stay_id
WHERE s3.sepsis3 IS TRUE
ORDER BY s3.sofa_score DESC;