from flask import Flask, request, jsonify
from dataHandler import get_data
import pandas as pd
from flask_cors import CORS
import json

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

    # Get the current annotation
    current_annotation = df[(df[annotations['x_value']] == annotations['x_coordinate']) & (df[annotations['y_value']] == annotations['y_coordinate'])]['annotations'].values[0]
    new_annotation = None

    # Now, you can update the annotation
    current_annotation = current_annotation.replace("'", "\"")  # Replace single quotes with double quotes
    new_annotation = json.loads(current_annotation) 
    new_annotation[annotations["plot_type"]]["x_coordinate"] = annotations['x_coordinate']  
    new_annotation[annotations["plot_type"]]["y_coordinate"] = annotations['y_coordinate']  
    new_annotation[annotations["plot_type"]]["annotation"] = annotations['annotation']  

    # Update the dataframe
    df.loc[(df['gdp_per_capita'] == annotations['x_coordinate']) & (df['health_expenditure'] == annotations['y_coordinate']), 'annotations'] = json.dumps(new_annotation)

    # for annotation in annotations:
    #     df.loc[df['id'] == annotation['id'], 'annotations'] = annotation['annotations']

    # Save updated dataframe into csv
    df.to_csv('data.csv', index=False)
    return jsonify({"message": "Annotations saved successfully"}), 200

# /api/annotated_scatter_points
@app.route('/annotated_scatter_points', methods=['GET'])
def get_annotated_scatter_points():
    df= get_data()
    sub_df= df[['id', 'annotations']].copy()
    sub_df['annotations'] = sub_df['annotations'].apply(lambda x: eval(x))
    result = sub_df[sub_df['annotations'].apply(lambda x: x['scatterPlot_annotations']['annotation'] != '')]
    # result = sub_df['annotations']
    json_data= result.to_json(orient='records')
    return json_data

# /api/annotated_heatmap_points
@app.route('/annotated_heatmap_points', methods=['GET'])
def get_annotated_heatmap_points():
    df= get_data()
    sub_df= df[['id', 'annotations']].copy()
    sub_df['annotations'] = sub_df['annotations'].apply(lambda x: eval(x))
    result = sub_df[sub_df['annotations'].apply(lambda x: x['heatMap_annotations']['annotation'] != '')]
    json_data= result.to_json(orient='records')
    return json_data

# /api/annotated_timeplot_points
@app.route('/annotated_timeplot_points', methods=['GET'])
def get_annotated_timeplot_points():
    df= get_data()
    sub_df= df[['id', 'annotations']].copy()
    sub_df['annotations'] = sub_df['annotations'].apply(lambda x: eval(x))
    result = sub_df[sub_df['annotations'].apply(lambda x: x['timePlot_annotations']['annotation'] != '')]
    json_data= result.to_json(orient='records')
    return json_data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)