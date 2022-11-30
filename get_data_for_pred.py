from Get_machines_attributes import get_machines_attributes
from Get_telemetry_data import get_telemetry_data


def get_data_for_pred(id, telemetry_list, attribute_list, start_date, end_date):
    import pandas as pd
    import psycopg2
    conn = psycopg2.connect(host="localhost", port=5434, database="rm_iiot", user="postgres", password="postgres")
    # ts_kv_dict = pd.read_csv('ts_kv_d.csv', index_col=0)
    sql = '''select * from ts_kv_dictionary;'''
    ts_kv_dict = pd.read_sql_query(sql, conn)

    telemetry_key = []
    for telemetry in telemetry_list:
        key = int(ts_kv_dict[ts_kv_dict['key'] == telemetry]['key_id'])
        telemetry_key.append(key)
    if len(telemetry_key) == 0:
        telemetry_key = [telemetry_key[0], telemetry_key[0]]
    telemetry_key = tuple(telemetry_key)
    sql = '''
        SELECT * FROM ts_kv 
        WHERE key IN {}
        AND
        entity_id = '{}'
        AND
        ts >= {}
        AND
        ts <= {}
    
        ;'''.format(tuple(telemetry_key), str(id), start_date, end_date)

    df = pd.read_sql_query(sql, conn)
    df = get_telemetry_data(df, telemetry_list, pd, conn)

    machine = df['entity_id'].unique()

    df_attribute = get_machines_attributes(machine, attribute_list, pd,conn)

    df = pd.merge(df, df_attribute, on='entity_id', how='left')
    return df
