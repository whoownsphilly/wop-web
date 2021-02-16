import { put, all, takeLatest } from "redux-saga/effects";
import axios from "axios";

import parsePropertySearchQuery from "../../../Utilities/queryHelpers";

import * as actionTypes from "./actionTypes";
import {
  setFirstName,
  setLastName,
  setSearchMethod,
  setSearchType,
  SubmitPropertySearchForm,
  setPropertyData,
} from "./actions";

function* submitSearchForm(action: SubmitPropertySearchForm): unknown {
  const { form, reject, resolve } = action;
  const { firstName, lastName, searchMethod, searchType } = form;

  let ownerName = `${lastName}`;
  if (firstName) {
    ownerName = `${lastName} ${firstName}`;
  }

  const query = parsePropertySearchQuery(ownerName, searchType);

  yield put(setSearchMethod(searchMethod));
  yield put(setSearchType(searchType));
  yield put(setFirstName(firstName));
  yield put(setLastName(lastName));

  let success = false;
  let data;

  yield axios
    .get(query)
    .then((res) => {
      const { status, data: resData } = res;

      if (status === 200) {
        success = true;
        data = resData;
      }
    })
    .catch((error) => {
      reject(error);
    });

  if (success && data) {
    yield put(setPropertyData(data));
    resolve();
  } else {
    reject("Something went horribly wrong...");
  }
}

function* watchsubmitSearchForm() {
  const { SUBMIT_PROPERTY_SEARCH_FORM } = actionTypes;

  yield takeLatest(SUBMIT_PROPERTY_SEARCH_FORM, submitSearchForm);
}

export default function* PropertiesRootSaga(): Generator {
  yield all([watchsubmitSearchForm()]);
}
