def get_unix_time2normal_time(df, datetime):
    df['ts'] = (df['ts'] / 1000).apply(lambda x: datetime.fromtimestamp(x))
    return df
