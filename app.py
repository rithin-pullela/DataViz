from flask import Flask, request, jsonify
from dataHandler import get_data
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    sub_df= df[['id','Country', 'Year','annotations', requested_column]].copy()
    json_data= sub_df.to_json(orient='records')
    return json_data

# /api/education_data
@app.route('/education_data', methods=['GET'])
def get_education_data():
    df= get_data()
    sub_df= df[['id','country', 'continent', 'year', 'avg_years_of_schooling', 'gdp_per_capita', 'life_expectancy', 'health_expenditure', 'electric_power_consumption', 'people_practicing_open_defecation','annotations']].copy()
    json_data= sub_df.to_json(orient='records')
    return json_data

# /api/save_annotations
@app.route('/save_annotations', methods=['POST'])
def save_annotations():
    df = get_data()
    annotations= request.get_json()
    for annotation in annotations:
        df.loc[df['id'] == annotation['id'], 'annotations'] = annotation['annotations']
    df.to_csv('data.csv', index=False)
    return jsonify({"message": "Annotations saved successfully"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)