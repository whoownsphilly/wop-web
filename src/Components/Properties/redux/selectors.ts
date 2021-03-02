import { RootState } from "../../../Store/RootReducer";
import { APISearchMethod, APISearchType } from "../../../Utilities/types";
import { Property, PropertyMetadata } from "../types";

export const selectPropertiesList = (state: RootState): Property[] => {
  return state.properties.data.properties;
};

export const selectPropertyMetadata = (state: RootState): PropertyMetadata => {
  return state.properties.data.metadata;
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
