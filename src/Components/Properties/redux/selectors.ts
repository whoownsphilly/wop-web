import { RootState } from "../../../Store/RootReducer";
import { APISearchMethod, APISearchType } from "../../../Utilities/types";
import { PropertyData } from "../types";

export const selectPropertiesList = (state: RootState): PropertyData => {
  return state.properties.data;
};

export const selectOwnerFirstName = (state: RootState): string => {
  return state.properties.firstName;
};

export const selectOwnerLastName = (state: RootState): string => {
  return state.properties.lastName;
};

export const selectSearchType = (state: RootState): APISearchType => {
  return state.properties.searchType;
};

export const selectSearchMethod = (state: RootState): APISearchMethod => {
  return state.properties.searchMethod;
};
