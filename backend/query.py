post = '''
INSERT INTO result(
      id
    , algorithm
    , dataset
    , roc_ys
    , roc_xs
    , actual_0
    , actual_1
    , predicted_0
    , predicted_1
    , f1_score
    , datetime
)
VALUES (
      :id
    , :algorithm
    , :dataset
    , :roc_ys
    , :roc_xs
    , :actual_0
    , :actual_1
    , :predicted_0
    , :predicted_1
    , :f1_score
    , :datetime
)
'''
# RETURNING id

get = '''
SELECT *
FROM result r
ORDER BY r.id
LIMIT :limit
OFFSET :offset
'''

get_all = '''
SELECT id, algorithm
FROM result
'''

get_by_id = '''
SELECT *
FROM result r
WHERE r.id = :id
LIMIT 1
'''

delete_by_id = '''
DELETE FROM result
WHERE id = :id
'''
