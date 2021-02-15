import { APISearchType, APISearchMethod } from "../../Utilities/types";

export interface Property {
  address: string;
}

export interface PropertyState {
  data: Property[];
  firstName: string;
  lastName: string;
  searchType: APISearchType;
  searchMethod: APISearchMethod;
}

export interface PropertySearchState {
  firstName: string;
  lastName: string;
  searchType: string;
  searchMethod: string;
}
