import { APISearchType } from "./types";

const parsePropertySearchQuery = (
  ownerName: string,
  searchType: APISearchType,
  searchMethod = null
): string => {
  const API_ENDPOINT = `/api/v1/properties`;

  const searchQueryString = `?search_query=${ownerName}`;
  const searchTypeString = `&search_type=${searchType}`;

  let searchMethodString = "";
  if (searchMethod) {
    searchMethodString = `&search_method=${searchMethod}`;
  }

  return `${API_ENDPOINT}${searchQueryString}${searchTypeString}${searchMethodString}`;
};

export default parsePropertySearchQuery;
