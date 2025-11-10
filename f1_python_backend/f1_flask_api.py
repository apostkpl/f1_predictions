from flask import Flask, jsonify, request
import pandas as pd
from f1_main import full_df, X_train, y_train, X_future, ids, predict_winner, pred_cols 

# Flask App Initialization
app = Flask(__name__)

def predict(grid: bool):
    # Get the relevant columns
    X_cols = pred_cols(grid = grid)
    
    # Split the dataset
    X_train_n = full_df[full_df['isPredictionData'] != 1][X_cols]
    y_train_n = full_df[full_df['isPredictionData'] != 1]['Winner']
    X_future_n = full_df[full_df['isPredictionData'] == 1][X_cols]
    
    # get the predictions using predict_winner() from f1_predictor.py
    results_df = predict_winner(X_train_n, y_train_n, X_future_n, ids)
    
    # Remove spaces from the column name, for it to work with json
    results_df.rename(columns = {'Probability to win': 'Probability_to_win'}, inplace = True)
    
    # Convert to records dictionary before converting to json
    return results_df.to_dict('records')

    
# Create the Endpoint for predictions
@app.route("/predict/next-race", methods = ["GET"])
def get_next_race():
    grid_param = request.args.get('grid', 'false').lower()
    grid = (grid_param == 'true')
    try:
        response_data = predict(grid = grid)
        return jsonify(response_data)
    except Exception as e:
        print(f"Prediction Error (Dynamic): {e}")
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

# Run the server on localhost
if __name__ == '__main__':
    # Flask runs on http://127.0.0.1:5000/ by default
    print("Starting Flask server...")
    app.run(debug = True)