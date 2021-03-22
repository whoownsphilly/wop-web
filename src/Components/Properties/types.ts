import { APISearchType, APISearchMethod } from "../../Utilities/types";

export interface PropertyMetadata {
  cartoDbTableName: string;
  searchToMatch: string;
  dataLinks: string[];
  searchMethod: string;
  searchQuery: string;
  searchType: string;
  title: string;
}

export interface Property {
  location: string;
  unit?: string;
  owner_1: string;
  owner_2?: string;
  mailing_care_of?: string;
  mailing_street?: string;
  mailingAddress1?: string;
  mailingAddress2?: string;
  mailing_city_state?: string;
  parcel_number?: string;
  building_code_description?: string;
  category_code_description?: string;
  homestead_exemption?: number;
  year_built?: string;
  year_built_estimate?: string;
  lat: number;
  lng: number;
  link_cyclomedia_street_view: string;
  link_property_phila_gov: string;
  link_atlas: string;
  link_license_inspections: string;
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
