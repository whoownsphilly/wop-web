import * as ActionTypes from "./actionTypes";
import { Property } from "../types";

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

export type Actions = GetPropertiesList;
