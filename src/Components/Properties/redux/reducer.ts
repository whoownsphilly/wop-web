/* eslint-disable no-case-declarations */
import * as ActionTypes from "./actionTypes";
import { Actions } from "./actions";
import { PropertyState } from "../types";

const initialState: PropertyState = {
  data: [],
};

const PropertyReducer = (
  state = initialState,
  action: Actions
): PropertyState => {
  const { type } = action;

  switch (type) {
    case ActionTypes.GET_PROPERTIES_LIST:
      const { data } = action;

      return { ...state, data };
    default:
      return state;
  }
};

export default PropertyReducer;
