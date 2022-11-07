DROP TABLE IF EXISTS result;

CREATE TABLE result(
    id UUID PRIMARY KEY,
    algorithm TEXT NOT NULL,
    dataset TEXT,
    roc_ys TEXT NOT NULL CHECK (roc_ys <> ''),
    roc_xs TEXT NOT NULL CHECK (roc_xs <> ''),
    actual_0 INTEGER CHECK (actual_0 >= 0),
    actual_1 INTEGER CHECK (actual_1 >= 0),
    predicted_0 INTEGER CHECK (predicted_0 >= 0),
    predicted_1 INTEGER CHECK (predicted_1 >= 0),
    f1_score FLOAT,
    datetime DATETIME NOT NULL
);

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
SELECT
      '07f64fa8-40a8-492f-98d6-9f5ee0aa6be4' AS id
     , 'detectron2_db_test' AS algorithm
     , null AS dataset
     , '0.6,0.5,0.2,0.4,0.1,0.1,0.4,0.3,0.0,0.9,0.0,0.2,0.0,0.3,0.7,0.4,0.8,0.0,0.1,0.2,0.6,0.7,0.3,0.8,0.0,0.5,0.5,0.9,0.2,0.3,0.4,0.6,0.4,0.9,0.1,0.4,0.1,0.3,0.5,0.1,0.2,0.4,0.1,0.3' AS roc_ys
     ,'0.6,0.5,0.2,0.4,0.1,0.1,0.4,0.3,0.0,0.9,0.0,0.2,0.0,0.3,0.7,0.4,0.8,0.0,0.1,0.2,0.6,0.7,0.3,0.8,0.0,0.5,0.5,0.9,0.2,0.3,0.4,0.6,0.4,0.9,0.1,0.4,0.1,0.3,0.5,0.1,0.2,0.4,0.1,0.3' AS roc_xs
     , 3862 AS actual_0
     , 155 AS actual_1
     , 782 AS predicted_0
     , 2005 AS predicted_1
     , 0.81 AS f1_score
     , datetime('now', 'localtime') AS datetime
;