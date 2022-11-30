def train_model(df, model, device_type):
    y_test = []
    y_pred = []
    path = ''

    if model == 'LGBM':
        y_test, y_pred, path = lgbm_model(df, device_type)
    elif model == 'LSTM':
        y_test, y_pred, path = lstm_model(df, device_type)

    precision, recall, roc_score, f1_score = get_model_score(y_test, y_pred)
    return precision, recall, roc_score, f1_score, path


def lgbm_model(df, device_type):
    x = df.drop(columns=['label', 'entity_id', 'ts'])
    y = df['label']
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    x = scaler.fit_transform(x)
    # print(x.shape)
    # from sklearn.model_selection import train_test_split
    # X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=.2,stratify=y)
    x_train = x  # temporary
    x_test = x  # temporary
    y_train = y  # temporary
    y_test = y  # temporary
    # print(X_train.shape)

    import lightgbm as lgb
    lgbm = lgb.LGBMClassifier(objective='binary')
    lgbm.fit(x_train, y_train)
    from datetime import datetime

    now = datetime.now()

    today = now.strftime("%d-%m-%Y_%H-%M-%S")

    import os
    path = os.getcwd()
    path = path + '\\Model/' + device_type + '_' + 'LGBM_'
    path = path + today
    import pickle
    pickle.dump(lgbm, open(path, 'wb'))
    y_pred = lgbm.predict(x_test)
    return y_test, y_pred, path


def lstm_model(df, device_type):
    x = df.drop(columns=['label', 'entity_id', 'ts'])
    y = df['label']
    # print(x)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    x = scaler.fit_transform(x)
    x = x.reshape(x.shape[0], 1, x.shape[1])
    # from sklearn.model_selection import train_test_split
    # X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=.2)
    X_train = x  # temporary
    X_test = x  # temporary
    Y_train = y  # temporary
    Y_test = y  # temporary

    # X_train=X_train.reshape(X_train[0],1,X_train[1])
    # X_test=X_test.reshape(X_test[0],1,X_test[1])

    from keras.models import Sequential
    from keras.layers import LSTM, Dropout, Dense

    model = Sequential()
    model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    model.fit(X_train, Y_train, epochs=50, batch_size=64, verbose=0, shuffle=False)

    from datetime import datetime

    now = datetime.now()

    today = now.strftime("%d-%m-%Y_%H-%M-%S")
    import os
    path = os.getcwd()  # current path
    path = path + '\\Model/' + device_type + '_LSTM' + '_' + today

    model.save(path)

    Y_pred = model.predict(X_test)

    Y_pred_b = []
    for i in Y_pred:
        if i > 0.5:
            Y_pred_b.append(1)
        else:
            Y_pred_b.append(0)

    return Y_test, Y_pred_b, path


def get_model_score(y_test, y_pred):
    from sklearn.metrics import precision_score, recall_score, roc_auc_score, f1_score

    Precision = precision_score(y_test, y_pred)
    Recall = recall_score(y_test, y_pred)
    Roc_score = roc_auc_score(y_test, y_pred)
    F1_score = f1_score(y_test, y_pred)

    return Precision, Recall, Roc_score, F1_score
