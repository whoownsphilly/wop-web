/* eslint-disable no-case-declarations */

import * as ActionTypes from "./actionTypes";
import { Actions } from "./actions";
import { HomeState } from "../types";

const initialState: HomeState = {
  apiVersion: "0",
};

const HomeReducer = (state = initialState, action: Actions): HomeState => {
  const { type } = action;

  switch (type) {
    case ActionTypes.GET_API_VERSION:
      const { data } = action;

      return { ...state, apiVersion: data };

    default:
      return state;
  }
};

export default HomeReducer;
