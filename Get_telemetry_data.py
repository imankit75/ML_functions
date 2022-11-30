import psycopg2


def get_telemetry_data(df, telemetry_list,
                       pd,conn):  # Takes a File and a list of telemetry and return a dataframe of list of telemetry ,
    # ts and id
    conn = psycopg2.connect(host="localhost", port=5434, database="rm_iiot", user="postgres", password="postgres")
    # ts_kv_dict = pd.read_csv('ts_kv_d.csv', index_col=0)
    sql = '''select * from ts_kv_dictionary;'''
    ts_kv_dict = pd.read_sql_query(sql, conn)

    key = int(ts_kv_dict[ts_kv_dict['key'] == telemetry_list[0]]['key_id'])
    telemetry = df[df['key'] == key].dropna(axis=1)
    telemetry.drop(columns='key', inplace=True)
    telemetry.columns = ['entity_id', 'ts', telemetry_list[0]]

    for i in range(1, len(telemetry_list)):
        key = int(ts_kv_dict[ts_kv_dict['key'] == telemetry_list[i]]['key_id'])
        temp = df[df['key'] == key].dropna(axis=1)
        temp.drop(columns='key', inplace=True)
        temp.columns = ['entity_id', 'ts', telemetry_list[i]]
        telemetry = pd.merge(telemetry, temp, on=['entity_id', 'ts'], how='left')

    return telemetry
