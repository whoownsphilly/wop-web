/* eslint-disable no-case-declarations */
import * as ActionTypes from "./actionTypes";
import { PropertyActions } from "./actions";
import { PropertyState } from "../types";

const initialState: PropertyState = {
  data: {
    metadata: {
      cartoDbLink: "",
      cartoDbTableName: "",
      odbLink: "",
      searchMethod: "",
      searchQuery: "",
      searchType: "",
      title: "",
    },
    properties: [],
  },
  firstName: "",
  lastName: "",
  searchType: "owner",
  searchMethod: "contains",
};

const PropertyReducer = (
  state: PropertyState = initialState,
  action: PropertyActions
): PropertyState => {
  switch (action.type) {
    case ActionTypes.SET_FIRST_NAME:
      const { firstName } = action;

      return { ...state, firstName };
    case ActionTypes.SET_LAST_NAME:
      const { lastName } = action;

      return { ...state, lastName };
    case ActionTypes.SET_SEARCH_TYPE:
      const { searchType } = action;

      return { ...state, searchType };
    case ActionTypes.SET_SEARCH_METHOD:
      const { searchMethod } = action;

      return { ...state, searchMethod };
    case ActionTypes.SET_PROPERTY_DATA:
      const { data: actionData } = action;

      return { ...state, data: actionData };
    default:
      return state;
  }
};

export default PropertyReducer;
