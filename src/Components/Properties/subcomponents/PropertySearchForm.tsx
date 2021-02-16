import React, { FunctionComponent } from "react";

import { PropertySearchState } from "../types";

interface Props {
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  searchState: PropertySearchState;
  updateSearchState: (searchState: PropertySearchState) => void;
}

const PropertySearchForm: FunctionComponent<Props> = (props: Props) => {
  const { handleSubmit, searchState, updateSearchState } = props;
  const { firstName, lastName, searchType, searchMethod } = searchState;

  const renderSearchForm = () => {
    return (
      <form onSubmit={(e) => handleSubmit(e)}>
        <label htmlFor="first-name">
          First Name:
          <input
            type="text"
            id="first-name"
            value={firstName}
            onChange={(e) =>
              updateSearchState({ ...searchState, firstName: e.target.value })
            }
          />
        </label>
        <label htmlFor="last-name">
          Last Name:
          <input
            type="text"
            id="last-name"
            value={lastName}
            onChange={(e) =>
              updateSearchState({
                ...searchState,
                lastName: e.target.value,
              })
            }
          />
        </label>
        <label htmlFor="search-type">
          Search Type:
          <select
            id="search-type"
            value={searchType}
            onChange={() =>
              updateSearchState({ ...searchState, searchType: "owner" })
            }
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
            onChange={() =>
              updateSearchState({
                ...searchState,
                searchMethod: "",
              })
            }
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
