from Get_telemetry_data import get_telemetry_data


def get_machine_data(device, telemetry_list, start_date, end_date, pd, conn):
    sql = '''SELECT * FROM device;'''

    device_data = pd.read_sql_query(sql, conn)

    # device_data = pd.read_csv('device_data.csv', index_col=0)

    machine_list = device_data[device_data['type'] == device]['id'].to_list()
    if len(machine_list) == 1:
        machine_list = [machine_list[0], machine_list[0]]

    machine_list = tuple(machine_list)

    sql = '''SELECT * FROM ts_kv_dictionary;'''
    ts_kv_dict = pd.read_sql_query(sql, conn)
    # ts_kv_dict = pd.read_csv('ts_kv_d.csv', index_col=0)
    telemetry_key_list = []
    for telemetry in telemetry_list:
        key = int(ts_kv_dict[ts_kv_dict['key'] == telemetry]['key_id'])
        telemetry_key_list.append(key)
    if len(telemetry_key_list) == 1:
        telemetry_key_list = [telemetry_key_list[0], telemetry_key_list[0]]
    telemetry_key_list = tuple(telemetry_key_list)
    # print(telemetry_key_list)

    sql = '''
    SELECT * FROM ts_kv 
    WHERE key IN {}
    AND
    entity_id IN {}
    AND
    ts >= {}
    AND
    ts <= {}

    ;'''.format(telemetry_key_list, machine_list, start_date, end_date)

    df = pd.read_sql_query(sql, conn)
    # print(df)
    df = get_telemetry_data(df, telemetry_list, pd, conn)

    return df
