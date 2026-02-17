SELECT DISTINCT 
    dia.subject_id,
    dia.hadm_id,
    dia.icd_code,
    dia.icd_version,
    d_icd.long_title
FROM mimiciv_hosp.diagnoses_icd dia
INNER JOIN mimiciv_hosp.d_icd_diagnoses d_icd 
    ON dia.icd_code = d_icd.icd_code 
    AND dia.icd_version = d_icd.icd_version
WHERE 
    -- ICD-9 Codes: Sepsis (038.x), Septicemia (995.91), Severe Sepsis (995.92), Septic Shock (785.52)
    (dia.icd_version = 9 AND (dia.icd_code LIKE '038%' OR dia.icd_code IN ('99591', '99592', '78552')))
    OR 
    -- ICD-10 Codes: A40 (Streptococcal), A41 (Other Sepsis), R65.2 (SIRS/Shock)
    (dia.icd_version = 10 AND (dia.icd_code LIKE 'A40%' OR dia.icd_code LIKE 'A41%' OR dia.icd_code LIKE 'R652%'));