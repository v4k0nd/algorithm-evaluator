# algorithm-evaluator

To install either 
```sh
pip install requirements.txt
```

Or manually install these two packages:

```
uvicorn[standard] fastapi
```

To run the evaluator
```sh
uvicorn main:app --reload
```

To test either open the webapp at the printed adress
```sh
http://127.0.0.1:8000
```

Or run a command from the `script` folder
```sh
./get_by_id 38a52d03-37e0-4d28-a7a8-3e800a633ce9 
```


## To reset database

The `generator.py` can create a new database from `initialiser.sql` (and adds one entry)
```sh
python3 generator.py init
```

If you would like to populate with more randomized examples
```sh
python3 generator.py populate
```


## Database structure
- `id`
    - :label: uuid
    - :memo: universally unique identifier
- `algorithm`
    - :label: text
    - :memo: contains name of the algorithm
- `dataset`
    - :label: text 
    - :memo: contains name of the dataset
- `roc_ys`
    - :label: text 
    - :memo: contains the y values for the ROC graph
    - example: 0.5,0.312,0.312,0.75,0.89,0.69
- `actual_0`
    - :label: text 
    - :memo: actual 0 from the confusion matrix
- `actual_1`
    - :label: text 
    - :memo: actual 1 from the confusion matrix
- `predicted_0`
    - :label: text 
    - :memo: predicted 0 from the confusion matrix
- `predicted_1`
    - :label: text 
    - :memo: predicted 1 from the confusion matix
- `f1_score`
    - :label: text 
    - :memo: contains the y values for the ROC graph
- `datatime`
    - :label: text 
    - :memo: time of initial run of the csv in the streamlit app