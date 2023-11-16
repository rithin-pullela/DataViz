from flask import Flask, request, jsonify
from dataHandler import get_data
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df= get_data()
    json_data = df.to_json(orient='records')
    return json_data

# /api/column_data?column=Population
@app.route('/column_data', methods=['GET'])
def get_col_country():
    df= get_data()
    requested_column= request.args.get('column')
    sub_df= df[['Country', 'Year', requested_column]].copy()
    json_data= sub_df.to_json(orient='records')
    return json_data

# /api/education_data
@app.route('/education_data', methods=['GET'])
def get_education_data():
    df= get_data()
    sub_df= df[['Country', 'Year', 'avg_years_of_schooling', 'GDP per capita', 'Life Expectancy', 'Health expenditure', 'Electric power consumption', 'People practicing open defecation']].copy()
    json_data= sub_df.to_json(orient='records')
    return json_data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)