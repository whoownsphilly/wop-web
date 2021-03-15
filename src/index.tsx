import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";

import ConfigureStore from "./Store/Store";

import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import App from "./App";

const store = ConfigureStore();

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);
