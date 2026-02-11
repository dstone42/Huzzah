WITH drug_list AS (
    SELECT UNNEST(ARRAY[
        -- PD-1 / PD-L1 Inhibitors
        'pembrolizumab', 'keytruda',
        'nivolumab', 'opdivo',
        'atezolizumab', 'tecentriq',
        'durvalumab', 'imfinzi',
        'avelumab', 'bavencio',
        'cemiplimab', 'libtayo',
        'dostarlimab', 'jemperli',
        'tislelizumab', 'tevimbra',
        'toripalimab', 'loqtorzi',
        -- CTLA-4 Inhibitors
        'ipilimumab', 'yervoy',
        'tremelimumab', 'imjudo',
        -- LAG-3 / TIGIT & Newer Checkpoints
        'relatlimab', 'opdualag', -- Opdualag is a combo (Nivo + Relat)
        'vibostolimab',
        'domvanalimab'
    ]) AS search_term
),
hits AS (
    SELECT 
        dl.search_term,
        mr.name AS found_name,
        mr.stay_id
    FROM drug_list dl
    JOIN mimiciv_ed.medrecon mr 
      ON mr.name ILIKE '%' || dl.search_term || '%'
)
SELECT 
    search_term,
    COUNT(DISTINCT stay_id) AS ed_visit_count,
    COUNT(*) AS total_mentions
FROM hits
GROUP BY search_term
ORDER BY ed_visit_count DESC;