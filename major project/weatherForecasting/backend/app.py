# Flask app placeholder
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from Independent_Analysis import Independent_Analysis
from Advanced_analysis import Advanced_analysis
import os
import uuid
import matplotlib.pyplot as plt

# Mapping of frontend parameter names to filenames and display names
paramToFile = {
    "Temperature (°C)": "cleaned_temp.csv",
    "Humidity": "cleaned_humidity2.csv",
    "Wind Speed (km/h)": "wind_speed_final.csv",
    "Air Pressure (hPa)": "FINAL_pressure.csv"
}

paramToDisp = {
    "Temperature (°C)": "Temperature (°C)",
    "Humidity": "Humidity",
    "Wind Speed (km/h)": "Wind Speed (km/h)",
    "Air Pressure (hPa)": "Air Pressure (hPa)"
}


app = Flask(__name__)
CORS(app)

# Paths
CSV_DIR = os.path.join(os.path.dirname(__file__), 'data')
PLOT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        payload = request.get_json()
        print("📥 Received payload:", payload)

        param = payload.get("parameter")  
        analysis = payload.get("analysisType") 
        cities = payload.get("cityList", []) 
        year_raw = payload.get("yearInput")

        if analysis in ["1","3", "6"]:
            if isinstance(year_raw, str):
                year_raw = year_raw.strip()
                year = int(year_raw) if year_raw else None
            elif isinstance(year_raw, int):
                year = year_raw
            else:
                year = None
        else:
            year = None

        print(f"param: {param}, analysis: {analysis}, cities: {cities}, year: {year}")

        data_path = os.path.join("data", paramToFile[param])
        print(f"📂 Loading data from: {data_path}")
        df = pd.read_csv(data_path, parse_dates=['datetime'], index_col='datetime')
        df = df.sort_index()
        df = df.select_dtypes(include=['number'])

        disp = paramToDisp[param]

        # Generate filename once
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.png"
        save_path = os.path.join(PLOT_DIR, filename)

        # Get city name from cityList or cityInput
        city_name = cities[0] if cities else payload.get("cityInput")

        if analysis == "independent" or analysis == "1":
            analyzer = Independent_Analysis(df, disp)
            analyzer.Monthly_pressure_analysis(city_name, year, save_path=save_path)
            img_path = f"/static/plots/{filename}"


        elif analysis == "2":
            if not city_name:
                return jsonify({"status": "error", "message": "City input is required for this analysis."}), 400
            analyzer = Independent_Analysis(df, disp)
            analyzer.Yearly_pressure_analysis(city_name, save_path=save_path)
            img_path = f"/static/plots/{filename}"

        
        elif analysis == "3":
            analyzer = Independent_Analysis(df, disp)
            unique_id = str(uuid.uuid4())

            # Handle both frontend key options: 'cityInput' and 'cityList'
            if cities and isinstance(cities, list) and len(cities) > 0:
                city_name = cities[0]
            else:
                city_name = payload.get("cityInput")

            # --- Monthly plot ---
            filename1 = f"{unique_id}_monthly.png"
            save_path1 = os.path.join(PLOT_DIR, filename1)
            analyzer.Monthly_pressure_analysis(city_name, year, save_path=save_path1)

            # --- Yearly plot ---
            filename2 = f"{unique_id}_yearly.png"
            save_path2 = os.path.join(PLOT_DIR, filename2)
            analyzer.Yearly_pressure_analysis(city_name, save_path=save_path2)

            # --- Hourly plot ---
            filename3 = f"{unique_id}_hourly.png"
            save_path3 = os.path.join(PLOT_DIR, filename3)
            analyzer.Hourly_Analysis(city_name, disp, save_path=save_path3)

            img_path = [f"/static/plots/{filename1}", f"/static/plots/{filename2}", f"/static/plots/{filename3}"]
        
        elif analysis == "5":
            if not city_name:
                return jsonify({"status": "error", "message": "City input is required for this analysis."}), 400

            analyzer = Independent_Analysis(df, disp)
            analyzer.Hourly_Analysis(city_name, disp, save_path=save_path)
            img_path = f"/static/plots/{filename}"

        elif analysis == "6":
            analyzer = Advanced_analysis(df, disp)
            image_paths = analyzer.monthly_yearly_analysis_template(year, cities, save_path=save_path)

            if image_paths:
                # Return list of image URLs (relative to /static)
                image_urls = ["/static/plots/" + os.path.basename(p) for p in image_paths]
                return jsonify({"status": "success", "images": image_urls})
            else:
                return jsonify({"status": "error", "message": "No images generated."}), 500


        else:
            return jsonify({"status": "error", "message": f"Unsupported analysis type: {analysis}"}), 400

        print(f"✅ Returning image path: /static/plots/{filename}")
        if isinstance(img_path, list):
            return jsonify({"status": "success", "images": img_path})
        else:
            return jsonify({"status": "success", "images": [img_path]})

    except Exception as e:
        print("❌ Error occurred:", e)
        return jsonify({"status": "error", "message": "Failed to process request."}), 500


if __name__ == '__main__':
    app.run(debug=True)
