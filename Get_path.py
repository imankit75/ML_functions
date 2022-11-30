def get_path(Device_type, algo, telemetry, attribute):
    import psycopg2
    import pandas as pd
    conn = psycopg2.connect(host="localhost", port=5432, database="dull", user="postgres", password="postgres")
    cursor = conn.cursor()
    sql = '''select * from equipment_models_predictive_maintenace'''
    df = pd.read_sql_query(sql, conn)

    df = df[(df['ai_ml_algo'] == algo) & (df['telemetry'] == " ".join(telemetry)) & (
                df['attributes'] == " ".join(attribute)) & (df['asset_id'] == Device_type)]
    df = df.sort_values('created_at_time', ascending=False, ignore_index=True)
    path = str(df['model_file_path'][0])
    return path