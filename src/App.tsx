import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import Properties from "./Components/Properties/Properties";
import Home from "./Components/Home/Home";
import "./App.css";

function App(): React.ReactElement {
  const [output, setOutput] = useState(0);

  useEffect(() => {
    fetch("/api/v1/properties?search_query=DOMB ALLAN&search_type=owner")
      .then((res) => res.json())
      .then((data) => {
        setOutput(data.results[0].location);
      });
  }, []);

  const renderRouter = () => {
    return (
      <Router>
        <div>
          <nav>
            <ul>
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/properties">Properties</Link>
              </li>
            </ul>
          </nav>

          <Switch>
            <Route path="/properties">
              <Properties />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </div>
      </Router>
    );
  };

  return (
    <div className="App">
      {renderRouter()}
      <p>The API output is {output}.</p>
    </div>
  );
}

export default App;
