def save_model_data(device_type, algorithm, precision, recall, roc_score, f1_score, path, telemetry_list, att_list,
                    start_date, end_date):
    import psycopg2
    conn = psycopg2.connect(host="localhost", port=5432, database="dull", user="postgres", password="postgres")
    cursor = conn.cursor()
    from datetime import date

    x = date.today()
    today = x.strftime("%d/%m/%Y")

    tel = " ".join(telemetry_list)
    att = " ".join(att_list)

    sql = """INSERT INTO equipment_models_predictive_maintenace 
    (asset_id,
    Model_File_Path,
    ai_ml_algo,
    precision_kpi,
    recall_kpi,
    roc_area,
    f1_score,
    last_trained_and_validated_on,
    telemetry,
    attributes,
    data_start_date,
    data_end_date
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    cursor.execute(sql, (
        device_type, path, algorithm, precision, recall, roc_score, f1_score, today, tel, att, start_date, end_date))
    conn.commit()
    conn.close()
