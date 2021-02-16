import { all } from "redux-saga/effects";

import PropertiesRootSaga from "../Components/Properties/redux/sagas";

export default function* RootSaga(): Generator {
  yield all([PropertiesRootSaga()]);
}
