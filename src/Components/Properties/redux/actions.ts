import * as ActionTypes from "./actionTypes";
import { Property, PropertySearchState } from "../types";
import { APISearchMethod, APISearchType } from "../../../Utilities/types";

interface GetPropertiesList {
  type: ActionTypes.GET_PROPERTIES_LIST;
  data: Property[];
}

export function getPropertiesList(data: Property[]): GetPropertiesList {
  const { GET_PROPERTIES_LIST } = ActionTypes;

  return {
    type: GET_PROPERTIES_LIST,
    data,
  };
}

interface SetFirstName {
  type: ActionTypes.SET_FIRST_NAME;
  firstName: string;
}

export function setFirstName(firstName: string): SetFirstName {
  const { SET_FIRST_NAME } = ActionTypes;

  return {
    type: SET_FIRST_NAME,
    firstName,
  };
}

interface SetLastName {
  type: ActionTypes.SET_LAST_NAME;
  lastName: string;
}

export function setLastName(lastName: string): SetLastName {
  const { SET_LAST_NAME } = ActionTypes;

  return {
    type: SET_LAST_NAME,
    lastName,
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

export type PropertyActions =
  | GetPropertiesList
  | SetFirstName
  | SetLastName
  | SetSearchType
  | SetSearchMethod
  | SubmitPropertySearchForm;
