import { createStore, applyMiddleware, Store } from "redux";
import { logger } from "redux-logger";
import { composeWithDevTools } from "redux-devtools-extension";

import { RootReducer, RootState, RootActionTypes } from "./RootReducer";

const ConfigureStore = (
  initialState?: RootState
): Store<RootState, RootActionTypes> => {
  const store = createStore(
    RootReducer,
    initialState,
    composeWithDevTools(applyMiddleware(logger))
  );

  return store;
};

export default ConfigureStore;
