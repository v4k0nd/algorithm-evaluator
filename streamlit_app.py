from typing import TYPE_CHECKING, List
import pandas as pd
import streamlit as st
from sklearn import metrics
from datetime import datetime
import uuid
import json
import requests
from rich import print as rprint
import matplotlib.pyplot as plt

# local imports
from script.roc_helper import create_roc_label, table_setup, conf_matrix_to_list
from model.Card import Card

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

# options
SAVE = True  # save to database the csv input
CSV_COLUMN_NAME_GROUND_TRUTH = "groundTruth"


# backend server
URL = 'http://algorithm-evaluator-back-end-1:8000'
URL_API = f"{URL}/api"

URL_POST = f"{URL_API}/result"
URL_GET_ALL = f"{URL_API}/results"
URL_GET_FULL = f"{URL_API}/results/full"
URL_GET_BY_ID = f"{URL_API}/result/id/"
URL_DELETE_ALL = f"{URL_API}/result/remove"

def clean_db():
    requests.delete(URL_DELETE_ALL)

def save_to_db(algorithm_name: str, conf_matrix_results: List[int], f1_score: float, y: list, X_confidence: list):
    # things to save to the database
    json_to_save = {}
    json_to_save['id'] = str(uuid.uuid4())
    json_to_save['algorithm'] = algorithm_name
    json_to_save['dataset'] = "artis10000"
    json_to_save['roc_ys'] = y.tolist()
    json_to_save['roc_xs'] = X_confidence.tolist()
    json_to_save['actual_0'] = conf_matrix_results[0]
    json_to_save['actual_1'] = conf_matrix_results[1]
    json_to_save['predicted_0'] = conf_matrix_results[2]
    json_to_save['predicted_1'] = conf_matrix_results[3]
    json_to_save['f1_score'] = f1_score
    json_to_save['datetime'] = datetime.now(
    ).isoformat(sep=" ", timespec="seconds")

    json_result = json.dumps(json_to_save, default=str)

    req = requests.post(URL_POST, json_result)


def find_algorithm_names(df: pd.DataFrame) -> list:
    algorithm_names = []
    for column_headers in df.columns:
        strsplit = column_headers.split("_")
        if len(strsplit) > 1:
            if strsplit[1] not in algorithm_names:
                algorithm_names.append(strsplit[1])
    return algorithm_names


def compute(y: list, X_confidence: list, threshold: float):
    return compute(y, X_confidence, X_label=create_roc_label(X_confidence, threshold))


def compute(y: list, X_confidence: list, X_label: list) -> Card:
    tn, fp, fn, tp = metrics.confusion_matrix(y, X_label).ravel()
    f1 = metrics.f1_score(y, X_label)
    
    # TODO try to implement merging multiple values, 
    #       https://scikit-learn.org/stable/visualizations.html#visualizations
    #      need to add new roc curve to `fig_roc`
    fig_roc = metrics.RocCurveDisplay.from_predictions(y, X_confidence) 
    
    fpr, tpr, thresholds = metrics.roc_curve(y, X_confidence)
    roc_auc = metrics.auc(fpr, tpr)
    # rprint("auc", roc_auc) 
    # fig_roc = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='example estimator')
    
    card_data = Card(fig_roc, tn, fp, fn, tp, f1)
    return card_data

def compute_multigraph(y, X_confidence, ax):
    return metrics.RocCurveDisplay.from_predictions(y, X_confidence, ax=ax, alpha=0.8)

def create_card(column: List["DeltaGenerator"], algorithm_name: str, card_data: Card):
    with column:
        st.subheader(algorithm_name)

        # ROC creation
        st.subheader("ROC curve")
        st.pyplot(card_data.get_fig().figure_)

        # Conf matrix creation
        st.subheader(f"Confidence matrix")
        df_table = card_data.get_conf_matrix_pd()
        st.table(df_table)

        # f1 score creation
        st.subheader("f1 score")
        st.text(card_data.get_f1())


if __name__ == "__main__":
    # x_label is for conf-matrix and f1 score
    # x_confidence is for ROC graph

    st.title("🧾 Algorithm evaluator ")
    st.text("Choose from previous database entries or upload csv")
    try:
        req = requests.get(URL_GET_ALL)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        st.error(
            f'{e.__class__.__name__}. Tried reaching backend for too long..', icon="🚨")
        res_json = []
    else:
        res_json = req.json()

    with st.form("dataset"):
        st.header('Retrieve from db')
        prepared_options = [e["algorithm"]+" - "+e["id"] for e in res_json]
        prepared_options.insert(0, "None")
        option = st.selectbox(
            'Choose which result would you like to use, if nothing appears, upload a csv first below.',
            index=0,
            help='format meaning: [algorithm name] - [UUID]',
            options=prepared_options,
        )
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            multi_figure = None
            # ax = None
            # ax = plt.gca()            
            try:
                id = option.split(" - ")[1]
                req = requests.get(f"{URL_GET_BY_ID}{id}")
                ret_json = req.json()

                y = ret_json["roc_ys"]
                X_confidence = ret_json["roc_xs"]
                X_label = create_roc_label(x_conf=X_confidence, threshold=0.5)

                algorithm_name = ret_json["algorithm"]
                column = st.columns(1, gap="medium")[0]
                
                card_data = compute(y, X_confidence, X_label)
                # multi_figure = compute_multigraph(y, X_confidence, ax)
                create_card(column, algorithm_name, card_data)
                
                # st.subheader("Multi ROC curve")
                # multi_figure.plot(ax=ax, alpha=0.5)
                # st.pyplot(multi_figure.figure_)
            except IndexError as e:
                st.error(
                    f'{e.__class__.__name__}. If there are no entries in the database, upload a csv and save results to the database 😄', icon="🚨")
    st.button('Clear DB',
              on_click=clean_db)
    st.header('CSV upload')
    
    agree = st.checkbox(
        'I want to save the result to the database.', value=True)
    uploaded_file = st.file_uploader("Choose a  CSV file", type=[
        'csv'], help="for each algorithm name an 'accuracy_' and 'labels_' columns is expected")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        alg_names = find_algorithm_names(df)
        columns = st.columns(len(alg_names), gap="medium")
        
        multi_figure = None
        ax = plt.gca()
        
        for i in range(0, len(alg_names)):
            algorithm_name = alg_names[i]
            column = columns[i]
            y = df[CSV_COLUMN_NAME_GROUND_TRUTH]
            X_confidence = df[f"accuracy_{algorithm_name}"]
            X_label = df[f"labels_{algorithm_name}"]
            card_data = compute(y, X_confidence, X_label)
            
            # save for generating a combined ROC graph
            multi_figure = compute_multigraph(y, X_confidence, ax)
            
            create_card(column, algorithm_name, card_data)
            if agree:
                save_to_db(algorithm_name, card_data.get_conf_matrix_list(
                ), card_data.get_f1(), y, X_confidence)
        
        st.subheader("Multi ROC curve")
        multi_figure.plot(ax=ax, alpha=0.5)
        st.pyplot(multi_figure.figure_)