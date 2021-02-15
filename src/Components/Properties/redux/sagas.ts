import { put, all, takeLatest } from "redux-saga/effects";

import * as actionTypes from "./actionTypes";
import { SubmitPropertySearchForm } from "./actions";

function* submitSearchForm(action: SubmitPropertySearchForm): Generator {
  const {
    SET_SEARCH_METHOD,
    SET_SEARCH_TYPE,
    SET_FIRST_NAME,
    SET_LAST_NAME,
  } = actionTypes;

  const { form } = action;
  const { firstName, lastName, searchMethod, searchType } = form;

  yield put({ type: SET_SEARCH_METHOD, searchMethod });
  yield put({ type: SET_SEARCH_TYPE, searchType });
  yield put({ type: SET_FIRST_NAME, firstName });
  yield put({ type: SET_LAST_NAME, lastName });
}

function* watchsubmitSearchForm() {
  const { SUBMIT_PROPERTY_SEARCH_FORM } = actionTypes;

  yield takeLatest(SUBMIT_PROPERTY_SEARCH_FORM, submitSearchForm);
}

export default function* PropertiesRootSaga(): Generator {
  yield all([watchsubmitSearchForm()]);
}
