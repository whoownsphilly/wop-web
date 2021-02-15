/** *****
 * API SEARCH TYPES
 */

/**
 * Options for different search types on the API
 * TODO Add more documentation on this
 */
export type APISearchType =
  | "owner"
  | "location_by_owner"
  | "location_by_mailing_address"
  | "mailing_address";

/**
 * Type API needs query in to search
 * TODO more information on this
 */
export type APISearchQuery = string;

/**
 * API Search Method
 * Optional
 * TODO add more documentation on how this affects search
 */
export type APISearchMethod = "contains" | "starts_with" | "ends_with" | "";
