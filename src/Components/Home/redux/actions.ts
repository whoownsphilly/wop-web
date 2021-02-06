import * as ActionTypes from "./actionTypes";

interface GetAPIVersion {
  type: ActionTypes.GET_API_VERSION;
  data: string;
}

export function getAPIVersion(data: string): GetAPIVersion {
  const { GET_API_VERSION } = ActionTypes;

  return {
    type: GET_API_VERSION,
    data,
  };
}

export type Actions = GetAPIVersion;
