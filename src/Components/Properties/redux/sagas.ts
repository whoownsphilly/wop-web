/* eslint-disable @typescript-eslint/naming-convention */
import { put, all, takeLatest } from "redux-saga/effects";
import axios from "axios";

import parseSearchQuery from "../../../Utilities/queryHelpers";

import * as actionTypes from "./actionTypes";
import {
  setSearchQuery,
  setSearchMethod,
  setSearchType,
  SubmitPropertySearchForm,
  setPropertyData,
} from "./actions";
import { PropertyMetadata } from "../types";

function* submitSearchForm(action: SubmitPropertySearchForm): unknown {
  const { form, reject, resolve } = action;
  const { searchQuery, searchMethod, searchType } = form;

  const ENDPOINT = `/api/v1/properties`;

  const query = parseSearchQuery(ENDPOINT, searchQuery, searchType);

  yield put(setSearchMethod(searchMethod));
  yield put(setSearchType(searchType));
  yield put(setSearchQuery(searchQuery));

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
    const { results, metadata } = data;
    const {
      title,
      cartodb_table_name,
      data_links,
      search_to_match,
      search_query,
      search_type,
      search_method,
    } = metadata;

    const transformedMetadata: PropertyMetadata = {
      title,
      cartoDbTableName: cartodb_table_name,
      dataLinks: data_links,
      searchToMatch: search_to_match,
      searchQuery: search_query,
      searchType: search_type,
      searchMethod: search_method,
    };

    const transformedData = {
      properties: results,
      metadata: transformedMetadata,
    };

    yield put(setPropertyData(transformedData));
    resolve();
  } else {
    reject("Something went horribly wrong submitting the search form.");
  }
}

function* watchsubmitSearchForm() {
  const { SUBMIT_PROPERTY_SEARCH_FORM } = actionTypes;

  yield takeLatest(SUBMIT_PROPERTY_SEARCH_FORM, submitSearchForm);
}

export default function* PropertiesRootSaga(): Generator {
  yield all([watchsubmitSearchForm()]);
}
