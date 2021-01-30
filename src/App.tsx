import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [output, setOutput] = useState(0);

  useEffect(() => {
    fetch('/api/v1/properties?search_query=DOMB ALLAN&search_type=owner').then(res => res.json()).then(data => {
      setOutput(data['results'][0]['location']);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The API output is {output}.</p>
      </header>
    </div>
  );
}

export default App;
