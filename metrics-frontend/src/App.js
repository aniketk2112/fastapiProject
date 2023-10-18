import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';

function App() {
  const [metrics, setMetrics] = useState({});
  const [selectedField, setSelectedField] = useState(null);
  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/metrics/');
        setMetrics(response.data);
      } catch (error) {
        console.error("Error fetching metrics", error);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    if (selectedField) {
      setData(metrics[selectedField.value]);
    }
  }, [selectedField, metrics]);

  const options = Object.keys(metrics).map(field => ({ value: field, label: field }));

  return (
    <div className="App">
      <header className="App-header">
        <h1>Metric Viewer</h1>
      </header>

      <section>
        <Select 
          options={options}
          onChange={setSelectedField}
          placeholder="Select a field..."
        />
      </section>

      <section>
        <h2>Data for: {selectedField?.label}</h2>
        <table>
          <thead>
            <tr>
              <th>Class</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row.class}</td>
                <td>{row[selectedField.value]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;
