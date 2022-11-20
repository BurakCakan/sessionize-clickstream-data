from fastapi import FastAPI
import dataPrep
import postgreConnector

raw_data = dataPrep.parse('https://storage.googleapis.com/xcc-de-assessment/events.json')

raw_df = dataPrep.to_dataframe(raw_data)

dataPrep.validation(raw_df)

df = dataPrep.calculate_sessionid(raw_df)

postgreConnector.write_to_pg(df, 'sessions')

results = postgreConnector.read_from_pg('results')

api_res = {
    'median_visits_before_order': results[0][0],
    'median_session_duration_minutes_before_order': results[0][1]
}

app = FastAPI()


@app.get("/metrics/orders")
def root():
    return api_res
