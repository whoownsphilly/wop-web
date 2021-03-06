import React, { ChangeEvent, FunctionComponent } from "react";
import { APISearchMethod, APISearchType } from "../../../Utilities/types";

import { PropertySearchState } from "../types";

interface Props {
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  searchState: PropertySearchState;
  updateSearchState: (searchState: PropertySearchState) => void;
}

const PropertySearchForm: FunctionComponent<Props> = (props: Props) => {
  const { handleSubmit, searchState, updateSearchState } = props;
  const { searchQuery, searchType, searchMethod } = searchState;

  const handleSearchMethodChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const { target } = event;
    const { value } = target;

    updateSearchState({
      ...searchState,
      searchMethod: value as APISearchMethod,
    });
  };

  const handleSearchTypeChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const { target } = event;
    const { value } = target;

    updateSearchState({
      ...searchState,
      searchType: value as APISearchType,
    });
  };

  const handleSearchQueryChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { target } = event;
    const { value } = target;

    updateSearchState({ ...searchState, searchQuery: value });
  };

  const renderSearchForm = () => {
    return (
      <form onSubmit={(e) => handleSubmit(e)}>
        <label htmlFor="search-query">
          Search Query:
          <input
            type="text"
            id="search-query"
            value={searchQuery}
            onChange={handleSearchQueryChange}
          />
        </label>
        <label htmlFor="search-type">
          Search Type:
          <select
            id="search-type"
            value={searchType}
            onChange={handleSearchTypeChange}
          >
            <option value="owner">Owner</option>
            <option value="location_by_owner">Location By Owner</option>
            <option value="location_by_mailing_address">
              Location By Mailing Address
            </option>
            <option value="mailing_address">Mailing Address</option>
          </select>
        </label>
        <label htmlFor="search-method">
          Search Method (Optional):
          <select
            id="search-method"
            value={searchMethod}
            onChange={handleSearchMethodChange}
          >
            <option value="">None</option>
            <option value="contains">Contains</option>
            <option value="starts_with">Starts With</option>
            <option value="ends_with">Ends With</option>
          </select>
        </label>
        <input type="submit" value="Search" />
      </form>
    );
  };

  return renderSearchForm();
};

export default PropertySearchForm;
