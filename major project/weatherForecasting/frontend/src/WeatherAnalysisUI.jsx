// WeatherAnalysisUI component
import React, { useState } from 'react';
import axios from 'axios';

const WeatherAnalysisUI = () => {
  const [parameter, setParameter] = useState('');
  const [analysisType, setAnalysisType] = useState('');
  const [yearInput, setYearInput] = useState('');
  const [cityInput, setCityInput] = useState('');
  const [cityList, setCityList] = useState(['']);
  const [imageUrls, setImageUrls] = useState([]);
  const [loading, setLoading] = useState(false);

  const paramToFile = {
  "Temperature (°C)": "data/cleaned_temp.csv",
  "Humidity": "data/cleaned_humidity2.csv",
  "Wind Speed (km/h)": "data/wind_speed_final.csv",
  "Air Pressure (hPa)": "data/FINAL_pressure.csv"};


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!parameter || !analysisType) {
      alert("Please select parameter and analysis type.");
      return;
    }

    const payload = {
      parameter,
      analysisType,
      yearInput,
      cityInput,
      cityList: cityList.filter(c => c.trim() !== ''),
      fileName: paramToFile[parameter]
    };

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/analyze', payload);
      let imageList = [];

      if (Array.isArray(response.data.images)) {
        imageList = response.data.images;
      } else if (response.data.image_path) {
        imageList = [response.data.image_path];
      }

      setImageUrls(imageList);
    } catch (err) {
      console.error("Error during analysis:", err);
      alert("Failed to process request. Check backend server.");
    } finally {
      setLoading(false);
    }
  };

  const handleCityChange = (index, value) => {
    const updated = [...cityList];
    updated[index] = value;
    setCityList(updated);
  };

  const addCity = () => {
    setCityList([...cityList, '']);
  };

  return (
    <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '8px' }}>
      <form onSubmit={handleSubmit}>
        <h2>📊 Choose Weather Analysis</h2>

        <label>Weather Parameter:</label>
        <select value={parameter} onChange={e => setParameter(e.target.value)}>
          <option value="">-- Select Parameter --</option>
          <option value="Temperature (°C)">Temperature (°C)</option>
          <option value="Humidity">Humidity</option>
          <option value="Wind Speed (km/h)">Wind Speed (km/h)</option>
          <option value="Air Pressure (hPa)">Air Pressure (hPa)</option>
        </select>

        <br /><br />

        <label>Analysis Type:</label>
        <select value={analysisType} onChange={e => setAnalysisType(e.target.value)}>
          <option value="">-- Select Type --</option>
          <option value="1">Monthly Analysis</option>
          <option value="2">Yearly Analysis</option>
          <option value="3">Monthly + Yearly + Hourly</option>
          <option value="5">Hourly Analysis</option>
          <option value="6">Advanced Analysis</option>
        </select>

        <br /><br />

        {(analysisType === "1" || analysisType === "3") && (
          <>
            <label>Year (2012-2017):</label>
            <input type="number" value={yearInput} onChange={e => setYearInput(e.target.value)} />
            <br /><br />
          </>
        )}

        {(["1", "2", "3", "5"].includes(analysisType)) && (
          <>
            <label>City:</label>
            <input type="text" value={cityInput} onChange={e => setCityInput(e.target.value)} />
            <br /><br />
          </>
        )}

        {analysisType === "6" && (
          <>
            <label>Year (Advanced Analysis):</label>
            <input type="number" value={yearInput} onChange={e => setYearInput(e.target.value)} />
            <br /><br />
            <label>Enter Cities:</label>
            {cityList.map((city, idx) => (
              <div key={idx}>
                <input
                  type="text"
                  value={city}
                  onChange={e => handleCityChange(idx, e.target.value)}
                />
              </div>
            ))}
            <button type="button" onClick={addCity}>Add Another City</button>
            <br /><br />
          </>
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Submit"}
        </button>
      </form>

      <hr style={{ margin: "2rem 0" }} />

      <div>
        {imageUrls.length > 0 && <h3>🖼️ Analysis Plots:</h3>}
        {imageUrls.map((url, idx) => (
          <div key={idx} style={{ marginBottom: '1rem' }}>
            <img
              src={`http://localhost:5000${url}`}
              alt={`Plot ${idx + 1}`}
              style={{ maxWidth: '100%', border: '1px solid #ccc', borderRadius: '6px' }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeatherAnalysisUI;
