# algorithm-evaluator

![Algorithm evaluator header](/docs/header.png)
### For automatically computing performance metrics for algorithms.
Powered by [Streamlit](https://streamlit.io/) <img src="https://streamlit.io/favicon.svg" width="20"> and [FastAPI](https://fastapi.tiangolo.com/) <img src="https://fastapi.tiangolo.com/img/favicon.png" width="20"> 

&nbsp;
<!-- 
## Features
### .csv upload
&nbsp;
![](/docs/csv_upload.png)

### Retrieve from db
&nbsp;

![](/docs/retrieve_from_db.png) -->

<!-- 
<p align="center">
  <img src="https://raw.githubusercontent.com/v4k0nd/algorithm-evaluator/master/docs/app_preview.png">
</p> -->

# Install and run via docker (recommended)
```sh
docker compose up [-d] # detached mode
```

The web-app should be available under http://localhost:8501, and upload a csv.


To stop the service, just `Ctrl + C`.


To remove installed container
```sh
docker compose down [-d] # detached mode
```

# Install and run locally
```sh
git clone https://github.com/v4k0nd/algorithm-evaluator.git
cd algorithm-evaluator
pip install -r requirements.txt
# or
pip install "uvicorn[standard]" fastapi jinja2 matplotlib sklearn pandas streamlit
```
## Starting the services

To start the backend
```sh
cd script
./start_backend.sh
```
Open a new terminal


Then start the frontend
```sh
cd script
./start_frontend.sh
```

Open the URL the `start_frontend.sh` gives (probably http://localhost:8501), and upload a csv.
<img src="https://raw.githubusercontent.com/v4k0nd/algorithm-evaluator/master/docs/streamlit_running.png">


# To reset database

The `generator.py` can create a new database from `initialiser.sql`
```sh
cd backend
python3 generator.py init
```

If you would like to populate with more randomized examples
```sh
cd backend
python3 generator.py populate
```


# Database structure
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
    - :label: list 
    - :memo: contains the y values for the ROC graph
    - example: 0.5,0.312,0.312,0.75,0.89,0.69
- `roc_ys`
    - :label: list 
    - :memo: contains the x values for the ROC graph
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