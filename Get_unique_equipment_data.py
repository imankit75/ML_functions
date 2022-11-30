def get_unique_equipment_data(Type, pd):  # Returns a part of ts_kv file of only one type of  Equipment

    df = pd.read_csv('ts_kv_b.csv', index_col=0, low_memory=False)
    device = pd.read_csv('device_data.csv', index_col=0)

    machine_list = device[device['type'] == Type]['id'].to_list()  # Return a list of ID of same type

    data = df[df['entity_id'] == machine_list[0]]
    for i in range(1, len(machine_list)):
        b = df[df['entity_id'] == machine_list[i]]  # temp variable
        c = pd.concat([data, b])  # temp variable
        data = c
    return data
