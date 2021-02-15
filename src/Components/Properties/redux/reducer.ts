/* eslint-disable no-case-declarations */
import * as ActionTypes from "./actionTypes";
import { PropertyActions } from "./actions";
import { PropertyState } from "../types";

const initialState: PropertyState = {
  data: [],
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
    case ActionTypes.GET_PROPERTIES_LIST:
      const { data } = action;

      return { ...state, data };

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
    default:
      return state;
  }
};

export default PropertyReducer;
