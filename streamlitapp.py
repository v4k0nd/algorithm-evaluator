import uuid
import pandas as pd
import streamlit as st
from rich import print as rprint
from sklearn import metrics
import streamlit as st
from datetime import datetime
import json
import requests

# options
save = True # save to database the csv input

# backend server
URL = 'http://localhost:8000'
URL_POST = f"{URL}/api/result"
URL_GET_ALL = f"{URL}/api/results"
URL_GET_FULL = f"{URL}/api/results/full"
URL_GET_BY_ID = f"{URL}/api/result/id/"



def find_algorithm_names(df):
    algorithm_names = []
    for column_headers in df.columns:
        strsplit = column_headers.split("_")
        if len(strsplit) > 1:
            if strsplit[1] not in algorithm_names:
                algorithm_names.append(strsplit[1])
    return algorithm_names


def table_setup(tn, fn, fp, tp):
    _data = [[str(tn),  str(fn)], [str(fp), str(tp)]]
    return pd.DataFrame(data=_data, index=['predicted 0', 'predicted 1'], columns=['actual 0', 'actual 1'])


def confusion_matrix_create(column_name, columnlabel, y, X):
    # y = df["groundTruth"] 
    # X = df[column_name]
    rprint("inside of y:\n",y)
    rprint("inside of x:\n",X)
    tn, fp, fn, tp = metrics.confusion_matrix(y, X).ravel()
   
    df_table = table_setup(tn, fp, fn, tp)
    columnlabel.table(df_table)
   
    f1 = metrics.f1_score(y, X)
    format_float_f1 = round(f1,3)
    card_f1 = f'<h3>F1 score</h3>\n<b>{format_float_f1}</b>'
    columnlabel.markdown(card_f1, unsafe_allow_html=True)
    return str(tn), str(tp), str(fn), str(fp), format_float_f1


def ROC_create(column_name, columnlabel, y, X):
    # y = df["groundTruth"]  # definite truth
    # X = df[column_name] # This should be the confidence scores and not the predicted labels
    # val_count = y.value_counts()
    # total = len(y)

    rprint(f"\nthe y values from csv \n{y}")
    rprint(f"\nthe X values from csv \n{X}")
    columnlabel.pyplot(fig_roc.figure_)
    return fig_roc


def show_results(algorithm_name, column_label, y, X):
    card_title = f'<h2>{algorithm_name.capitalize()} results</h2>'
    card_roc = '<h3> ROC curve </h3>'
    card_conf_m = '<h3> Confusion matrix</h3>'
    column_label.markdown(card_title, unsafe_allow_html=True)
#     st.write (algorithm_name+ " algorithm results")
    column_label.markdown(card_roc, unsafe_allow_html=True)
    fig_ROC = ROC_create("accuracy_"+algorithm_name, column_label, y, X)
    column_label.markdown(card_conf_m, unsafe_allow_html=True)
    conf_matrix_results = confusion_matrix_create(
        "labels_"+algorithm_name, column_label, y, X)
    
    if save == True:
        save_to_db(algorithm_name, conf_matrix_results, "labels_"+algorithm_name, y, X)
    # ROC to string
    #X = np.array(fig_ROC.figure_.canvas.renderer.buffer_rgba())
    # print(fig_ROC)

def save_to_db(algorithm_name, conf_matrix_results, column_label, y, X):
    # things to save to the database
    json_to_save = {}
    json_to_save['id'] = str(uuid.uuid4())
    json_to_save['algorithm'] = algorithm_name
    json_to_save['dataset'] = "artis10000"
    json_to_save['roc_ys'] = y.tolist() # df["groundTruth"].tolist()
    json_to_save['roc_xs'] = X.tolist() # df[column_label].tolist()
    json_to_save['actual_0'] = conf_matrix_results[0]
    json_to_save['actual_1'] = conf_matrix_results[1]
    json_to_save['predicted_0'] = conf_matrix_results[2]
    json_to_save['predicted_1'] = conf_matrix_results[3]
    json_to_save['f1_score'] = conf_matrix_results[4]
    json_to_save['datetime'] = datetime.now().isoformat(sep=" ", timespec="seconds")

    json_result = json.dumps(json_to_save, default=str)

    req = requests.post(URL_POST, json_result)
    rprint(f"\nresponse from request: {req.text}")

def select_result(id):
    req = requests.get(f"{URL_GET_BY_ID}{id}")
    # req = requests.get(f"{URL_GET_BY_ID}{st.session_state['id']}")
    ret_json = req.json()
    print(ret_json)
    y = ret_json["roc_ys"]
    X = ret_json["roc_xs"]
    alg_name = ret_json["algorithm"]
    column_label =  st.columns(3, gap="medium")[0]
    card_title = f'<h2>{alg_name} results</h2>'
    column_label.markdown(card_title, unsafe_allow_html=True)
#     st.write (algorithm_name+ " algorithm results")
    
    card_roc = '<h3> ROC curve </h3>'
    column_label.markdown(card_roc, unsafe_allow_html=True)
    fig_ROC = ROC_create("accuracy_"+alg_name, column_label, y, X)
    
    card_conf_m = '<h3> Confusion matrix</h3>'
    column_label.markdown(card_conf_m, unsafe_allow_html=True)
    
    tn, fp, fn, tp = metrics.confusion_matrix(y, X).ravel()
    df_table = table_setup(tn, fp, fn, tp)
    column_label.table(df_table)

    f1 = metrics.f1_score(y, X)
    format_float_f1 = round(f1,3)
    card_f1 = f'<h3>F1 score</h3>\n<b>{format_float_f1}</b>'
    column_label.markdown(card_f1, unsafe_allow_html=True)
    # print(dff)
    # print(str(tn))
    # print(str(tp))
    return str(tn), str(tp), str(fn), str(fp), format_float_f1
    
    
def select_helper():
    print("option: ",option)

req = requests.get(URL_GET_ALL)
rprint(f"\nRequesting all algname and id: {req.text}")
res_json = req.json()

with st.form("dataset"):
    prepared_options = [e["algorithm"]+" - "+e["id"] for e in res_json]
    prepared_options.insert(0, "None")
    option = st.selectbox(
        'Which result would you like to use',
        index=0,
        options=prepared_options,
        # on_change=select_helper, 
        # args=option.split(" - ")[1]
        )
    submitted = st.form_submit_button("Submit")
    if submitted:
        select_result(option.split(" - ")[1])

# print(res_json)
# prepared_options = {"0": "None"}
# for e in res_json:
#     prepared_options[e["id"]] = e["algorithm"]
    
# option = st.selectbox('Which result would you like to use', 
#                       prepared_options.keys(), 
#                       format_func=lambda x:prepared_options[ x ])

# st.write('You selected:', option)


uploaded_file = st.file_uploader("Choose a  CSV file", type=['csv'])


if uploaded_file is not None:
    # read csv
    df = pd.read_csv(uploaded_file)
    algorithm_results = []
    temp_test = find_algorithm_names(df)
    columns = st.columns(len(temp_test), gap="medium")
    for i in range(0, len(temp_test)):
        rprint(columns[i])
        y = df["groundTruth"]
        X_acc = df["accuracy_"+temp_test[i]]
        X_label = df["label_"+temp_test[i]]
        algorithm_results.append(show_results(temp_test[i], columns[i], y, X_acc, X_label))
        
