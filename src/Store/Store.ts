import { createStore, applyMiddleware, Store } from "redux";
import { logger } from "redux-logger";

import { RootReducer, RootState, RootActionTypes } from "./RootReducer";

const ConfigureStore = (
  initialState?: RootState
): Store<RootState, RootActionTypes> => {
  const store = createStore(RootReducer, initialState, applyMiddleware(logger));

  return store;
};

export default ConfigureStore;
