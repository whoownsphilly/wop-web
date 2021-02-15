import { put, all, takeLatest } from "redux-saga/effects";
import axios from "axios";

import * as actionTypes from "./actionTypes";
import {
  setFirstName,
  setLastName,
  setSearchMethod,
  setSearchType,
  SubmitPropertySearchForm,
} from "./actions";

function* submitSearchForm(action: SubmitPropertySearchForm): unknown {
  const { form, reject, resolve } = action;
  const { firstName, lastName, searchMethod, searchType } = form;

  let ownerName = `${lastName}`;
  if (firstName) {
    ownerName = `${lastName} ${firstName}`;
  }

  const API_ENDPOINT = `/api/v1/properties`;
  const SEARCH_QUERY = `?search_query=${ownerName}`;
  const SEARCH_TYPE = `&search_type=${searchType}`;
  const QUERY = `${API_ENDPOINT}${SEARCH_QUERY}${SEARCH_TYPE}`;

  yield put(setSearchMethod(searchMethod));
  yield put(setSearchType(searchType));
  yield put(setFirstName(firstName));
  yield put(setLastName(lastName));

  axios
    .get(QUERY)
    .then((res) => {
      const { data } = res;
      console.log(data);

      resolve();
    })
    .catch((error) => {
      console.error(error);

      reject(error);
    });
}

function* watchsubmitSearchForm() {
  const { SUBMIT_PROPERTY_SEARCH_FORM } = actionTypes;

  yield takeLatest(SUBMIT_PROPERTY_SEARCH_FORM, submitSearchForm);
}

export default function* PropertiesRootSaga(): Generator {
  yield all([watchsubmitSearchForm()]);
}
