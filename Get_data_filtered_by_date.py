def get_data_filtered_by_date(df,start_date,end_date):
    data=df [ (df['ts']>=int(start_date)) & ( df['ts']<=int(end_date) ) ]
    return data