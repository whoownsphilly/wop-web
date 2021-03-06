import { APISearchType, APISearchMethod } from "../../Utilities/types";

export interface PropertyMetadata {
  cartoDbLink: string;
  cartoDbTableName: string;
  odbLink: string;
  searchMethod: string;
  searchQuery: string;
  searchType: string;
  title: string;
}

export interface Property {
  lat: number;
  lng: number;
  location: string;
  mailingAddress1?: string;
  mailingAddress2?: string;
  mailing_care_of?: string;
  mailing_city_state?: string;
  owner_2?: string;
  parcel_number?: string;
  unit?: string;
}

export interface PropertyData {
  metadata: PropertyMetadata;
  properties: Property[];
}

export interface PropertyState {
  data: PropertyData;
  searchQuery: string;
  searchType: APISearchType;
  searchMethod: APISearchMethod;
}

export interface PropertySearchState {
  searchQuery: string;
  searchType: APISearchType;
  searchMethod: APISearchMethod;
}
