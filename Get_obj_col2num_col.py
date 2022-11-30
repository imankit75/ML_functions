def get_obj_col2num_col(df):  # changes object columns to numerical columns

    df.fillna(0, inplace=True)

    all_cols = df.columns.to_list()
    num_cols = df.describe().columns.to_list()
    obj_cols = [col for col in all_cols if col not in num_cols]

    from sklearn.preprocessing import LabelEncoder

    for col in obj_cols:
        label = LabelEncoder()
        df[col] = label.fit_transform(df[col])
    return df
