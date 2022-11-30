def get_machines_attributes(machine_list, attribute_list, pd, conn):
    # attribute_file = pd.read_csv('Attribute_kv.csv', index_col=0)
    # import psycopg2
    # conn = psycopg2.connect(host="localhost", port=5434, database="rm_iiot", user="postgres", password="postgres")
    sql = '''SELECT * from attribute_kv;'''
    attribute_file = pd.read_sql_query(sql, conn)
    data = get_one_machine_attributes(machine_list[0], attribute_list, attribute_file, pd)

    for i in range(1, len(machine_list)):
        df = get_one_machine_attributes(machine_list[i], attribute_list, attribute_file, pd)
        data = pd.concat([data, df], join='outer', ignore_index=True)
    return data


def get_one_machine_attributes(entity_id, att_list, att_file, pd):
    r = att_file[att_file['entity_id'] == entity_id]  # temp variable

    df = r[r['attribute_key'] == att_list[0]]
    df.dropna(axis=1, inplace=True)
    df.drop(columns=['entity_type', 'attribute_type', 'last_update_ts', 'attribute_key'], inplace=True)
    df.columns = ['entity_id', att_list[0]]

    for i in range(1, len(att_list)):
        at = r[r['attribute_key'] == att_list[i]]  # temp variable
        at.dropna(axis=1, inplace=True)
        at.drop(columns=['entity_type', 'attribute_type', 'last_update_ts', 'attribute_key'], inplace=True)
        at.columns = ['entity_id', att_list[i]]
        df = pd.merge(df, at, on='entity_id', how='left')

    return df
