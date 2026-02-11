-- Focus: Sepsis-3 patients on Pembrolizumab (Outpatient/MedRecon)
WITH pembro_users AS (
    -- Look for pembrolizumab in the ED medication reconciliation
    -- This table represents what they were taking BEFORE admission
    SELECT DISTINCT 
        stay_id, 
        subject_id,
        name AS drug_name
    FROM mimiciv_ed.medrecon
    WHERE name ILIKE '%pembrolizumab%' 
       OR name ILIKE '%keytruda%'
)
SELECT 
    s3.subject_id,
    s3.stay_id,
    s3.sofa_score,
    s3.suspected_infection_time,
    pu.drug_name,
    ed.intime AS ed_arrival,
    ed.outtime AS ed_departure
FROM mimiciv_derived.sepsis3 s3
INNER JOIN pembro_users pu 
    ON s3.stay_id = pu.stay_id
INNER JOIN mimiciv_ed.edstays ed 
    ON s3.stay_id = ed.stay_id
WHERE s3.sepsis3 IS TRUE;