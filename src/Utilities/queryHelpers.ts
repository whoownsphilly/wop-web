import { APISearchType } from "./types";

const parseSearchQuery = (
  endpoint: string,
  searchQuery: string,
  searchType: APISearchType,
  searchMethod = null
): string => {
  const searchQueryString = `?search_query=${searchQuery}`;
  const searchTypeString = `&search_type=${searchType}`;

  let searchMethodString = "";
  if (searchMethod) {
    searchMethodString = `&search_method=${searchMethod}`;
  }

  return `${endpoint}${searchQueryString}${searchTypeString}${searchMethodString}`;
};

export default parseSearchQuery;
