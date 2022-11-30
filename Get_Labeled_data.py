def label_equipment_failure_data(df, hr,pd):
    from datetime import datetime
    df['label'] = 0

    id_list = df['entity_id'].unique()
    issue = pd.read_excel('issue (6).xlsx')  # issue Table
    for entity_id in id_list:
        timestamp = issue[issue['workcenter_id'] == entity_id]['reported_datetime']

        for ts in timestamp:
            # print(ts,type(ts))
            ts = datetime.fromtimestamp(int(ts) / 1000)

            df = get_label_data_for_one_machine_and_one_timestamp(df, entity_id, ts, hr)
    return df


def get_label_data_for_one_machine_and_one_timestamp(df, entity_id, ts, hr):
    from datetime import timedelta
    t = timedelta(hours=hr)
    # print(type(ts),type(t))
    t_start = ts - t
    t_end = ts
    df['label'][(df['ts'] >= t_start) & (df['ts'] <= t_end) & (df['entity_id'] == entity_id)] = 1
    return df
