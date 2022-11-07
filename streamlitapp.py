import uuid
import pandas as pd
import streamlit as st
from rich import print as rprint
from sklearn import metrics
import streamlit as st
import datetime
import random
import json
import requests

# backend server
URL = 'http://localhost:8000'
URL_POST = f"{URL}/api/result"
URL_GET_ALL = f"{URL}/api/results"
URL_GET_BY_ID = f"{URL}/id/"

def find_algorithm_names(df):
    algorithm_names = []
    for column_headers in df.columns:
        strsplit = column_headers.split("_")
        if len(strsplit) > 1:
            if strsplit[1] not in algorithm_names:
                algorithm_names.append(strsplit[1])
    return algorithm_names


def table_setup():
    d = {' ': ["actual 0", "actual 1"], 'predicted 0': [
        "0", "0"], 'predicted 1': ["0", "0"]}
    dff = pd.DataFrame(data=d)
    return dff


def confusion_matrix_create(column_name, columnlabel):
    y = df["groundTruth"]  # definite truth
    val_count = y.value_counts()
    total = len(y)
    dff = table_setup()

    X = df[column_name]
    # continue
    tn, fp, fn, tp = metrics.confusion_matrix(y, X).ravel()

    f1 = metrics.f1_score(y, X)

    dff['predicted 0'] = [str(tn), str(fn)]
    dff['predicted 1'] = [str(fp), str(tp)]

    blankIndex = [''] * len(dff)
    dff.index = blankIndex
    columnlabel.table(dff)
    new_title1 = '<p style="font-family:sans-serif;  font-size: 36px;">'
    format_float_f1 = "{:.2f}".format(f1)
    new_title2 = 'F1 score: ' + str(format_float_f1)+'</p>'
    new_title = new_title1+new_title2
    columnlabel.markdown(new_title, unsafe_allow_html=True)
    # print(dff)
    # print(str(tn))
    # print(str(tp))
    return str(tn), str(tp), str(fn), str(fp), format_float_f1


def ROC_create(column_name, columnlabel):
    y = df["groundTruth"]  # definite truth
    val_count = y.value_counts()
    total = len(y)

    X = df[column_name]
    rprint(f"\nthe y values from csv \n{y}")
    rprint(f"\nthe X values from csv \n{X}")
    fig_roc = metrics.RocCurveDisplay.from_predictions(y, X)
#     plt.show()
    columnlabel.pyplot(fig_roc.figure_)
    return fig_roc


def show_results(algorithm_name, column_label):
    # new_title1 = '<p style="font-family:sans-serif;  font-size: 34px;">'
    # new_title2 = algorithm_name.capitalize()+' results</p>'
    card_title = f'<h2>{algorithm_name.capitalize()} results</h2>'
    card_roc = f'<h3> ROC curve </h3>'
    card_conf_m = '<h3> Confusion matrix</h3>'
    column_label.markdown(card_title, unsafe_allow_html=True)
#     st.write (algorithm_name+ " algorithm results")
    column_label.markdown(card_roc, unsafe_allow_html=True)
    fig_ROC = ROC_create("accuracy_"+algorithm_name, column_label)
    column_label.markdown(card_conf_m, unsafe_allow_html=True)
    conf_matrix_results = confusion_matrix_create(
        "labels_"+algorithm_name, column_label)
    
    save_to_db(algorithm_name, conf_matrix_results, "labels_"+algorithm_name)
    # ROC to string
    #X = np.array(fig_ROC.figure_.canvas.renderer.buffer_rgba())
    # print(fig_ROC)

def save_to_db(algorithm_name, conf_matrix_results, column_label):
    current_time = datetime.datetime.now()
    d = current_time.strftime("%m/%d/%Y, %H:%M:%S")

    # things to save to the database
    json_to_save = {}
    json_to_save['id'] = str(uuid.uuid4())
    json_to_save['algorithm'] = algorithm_name
    json_to_save['dataset'] = "artis10000"
    json_to_save['roc_ys'] = df["groundTruth"].tolist()
    json_to_save['roc_xs'] = df[column_label].tolist()
    json_to_save['actual_0'] = conf_matrix_results[0]
    json_to_save['actual_1'] = conf_matrix_results[1]
    json_to_save['predicted_0'] = conf_matrix_results[2]
    json_to_save['predicted_1'] = conf_matrix_results[3]
    json_to_save['f1_score'] = conf_matrix_results[4]
    json_to_save['datetime'] = d

    json_result = json.dumps(json_to_save)

    req = requests.post(URL_POST, json_result)
    rprint(f"\nresponse from request: {req.text}")

def select_result(id):
    req = requests.get(f"{URL_GET_BY_ID}{id}")
    

req = requests.get(URL_GET_ALL)
rprint(f"\nresponse from request: {req.text}")
prepared_options = [e["algorithm"]+" - "+e["id"] for e in req.json()]
prepared_options.insert(0, "None")
option = st.selectbox(
    'Which result would you like to use',
    options=prepared_options,
    # on_change=select_result, 
    # args=option.split(" - ")[1]
    )

st.write('You selected:', option)
uploaded_file = st.file_uploader("Choose a  CSV file", type=['csv'])


if uploaded_file is not None:
    # read csv
    df = pd.read_csv(uploaded_file)
    algorithm_results = []
    temp_test = find_algorithm_names(df)
    columns = st.columns(len(temp_test), gap="medium")
    for i in range(0, len(temp_test)):
        algorithm_results.append(show_results(temp_test[i], columns[i]))
        
