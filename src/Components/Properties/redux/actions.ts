import * as ActionTypes from "./actionTypes";
import { PropertySearchState, PropertyData } from "../types";
import { APISearchMethod, APISearchType } from "../../../Utilities/types";

interface SetSearchQuery {
  type: ActionTypes.SET_SEARCH_QUERY;
  searchQuery: string;
}

export function setSearchQuery(searchQuery: string): SetSearchQuery {
  const { SET_SEARCH_QUERY } = ActionTypes;

  return {
    type: SET_SEARCH_QUERY,
    searchQuery,
  };
}

interface SetSearchType {
  type: ActionTypes.SET_SEARCH_TYPE;
  searchType: APISearchType;
}

export function setSearchType(searchType: APISearchType): SetSearchType {
  const { SET_SEARCH_TYPE } = ActionTypes;

  return {
    type: SET_SEARCH_TYPE,
    searchType,
  };
}

interface SetSearchMethod {
  type: ActionTypes.SET_SEARCH_METHOD;
  searchMethod: APISearchMethod;
}

export function setSearchMethod(
  searchMethod: APISearchMethod
): SetSearchMethod {
  const { SET_SEARCH_METHOD } = ActionTypes;

  return {
    type: SET_SEARCH_METHOD,
    searchMethod,
  };
}

export interface SubmitPropertySearchForm {
  type: ActionTypes.SUBMIT_PROPERTY_SEARCH_FORM;
  form: PropertySearchState;
  resolve: () => void;
  reject: (errorMessage: string) => void;
}

export function submitPropertySearchForm(
  form: PropertySearchState,
  resolve: () => void,
  reject: (errorMessage: string) => void
): SubmitPropertySearchForm {
  const { SUBMIT_PROPERTY_SEARCH_FORM } = ActionTypes;

  return {
    type: SUBMIT_PROPERTY_SEARCH_FORM,
    form,
    resolve,
    reject,
  };
}

export interface SetPropertyData {
  type: ActionTypes.SET_PROPERTY_DATA;
  data: PropertyData;
}

export function setPropertyData(data: PropertyData): SetPropertyData {
  const { SET_PROPERTY_DATA } = ActionTypes;

  return {
    type: SET_PROPERTY_DATA,
    data,
  };
}

export type PropertyActions =
  | SetSearchQuery
  | SetSearchType
  | SetSearchMethod
  | SubmitPropertySearchForm
  | SetPropertyData;
