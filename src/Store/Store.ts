import { createStore, applyMiddleware, Store } from "redux";
import { logger } from "redux-logger";
import { composeWithDevTools } from "redux-devtools-extension";
import createSagaMiddleware from "redux-saga";

import { RootReducer, RootState, RootActionTypes } from "./RootReducer";
import RootSaga from "./RootSaga";

const sagaMiddleware = createSagaMiddleware();

const ConfigureStore = (
  initialState?: RootState
): Store<RootState, RootActionTypes> => {
  const store = createStore(
    RootReducer,
    initialState,
    composeWithDevTools(
      applyMiddleware(logger),
      applyMiddleware(sagaMiddleware)
    )
  );

  sagaMiddleware.run(RootSaga);

  return store;
};

export default ConfigureStore;
