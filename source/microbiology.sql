SELECT 
    micro.subject_id, 
    micro.hadm_id, 
    micro.charttime,
    -- Specimen and Test information
    micro.spec_type_desc, 
    micro.test_name,
    -- Organism found
    micro.org_name,
    -- Antimicrobial Sensitivity details
    micro.ab_name,
    micro.interpretation, -- S (Susceptible), R (Resistant), I (Intermediate)
    micro.dilution_text,
    micro.dilution_comparison,
    micro.dilution_value,
    -- Metadata and comments
    micro.storetime,
    micro.comments
FROM mimiciv_hosp.microbiologyevents AS micro
ORDER BY 
    micro.subject_id, 
    micro.charttime, 
    micro.org_name;