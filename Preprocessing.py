from Get_machines_attributes import get_machines_attributes
from Get_unix_time2normal_time import get_unix_time2normal_time
from Get_obj_col2num_col import get_obj_col2num_col
from Get_Labeled_data import label_equipment_failure_data
from ML_Pycharm.Get_machine_data import get_machine_data
from Training import train_model
from Insert_into_sql_table import save_model_data


def build_ai_model(device_type, algorithm, attribute_list, telemetry_list, start_date, end_date,
                   number_of_hrs_for_marking):
    import pandas as pd
    from datetime import datetime
    import psycopg2
    conn = psycopg2.connect(host="localhost", port=5434, database="rm_iiot", user="postgres", password="postgres")

    df_machine = get_machine_data(device_type, telemetry_list, start_date, end_date, pd, conn)
    # print(df_machine, df_machine.columns)

    machine_list = df_machine['entity_id'].unique()  # returns array of unique machine ID in df_date

    df = get_machines_attributes(machine_list, attribute_list, pd, conn)

    df = pd.merge(df_machine, df, on='entity_id', how='left')

    df = get_unix_time2normal_time(df, datetime)

    df = label_equipment_failure_data(df, number_of_hrs_for_marking, pd)
    # print(df)

    df = get_obj_col2num_col(df)

    precision, recall, roc_score, f1_score, path = train_model(df, algorithm, device_type)
    start_date = datetime.fromtimestamp(start_date / 1000)
    start_date = start_date.strftime("%d/%m/%Y")
    end_date = datetime.fromtimestamp(end_date / 1000)
    end_date = end_date.strftime("%d/%m/%Y")
    # print(precision, recall, roc_score, f1_score, path)
    save_model_data(device_type, algorithm, precision, recall, roc_score, f1_score, path, telemetry_list,
                    attribute_list, start_date, end_date)  # insert precision score,Recall score and area under ROC
    # curve into SQL table
    conn.close()