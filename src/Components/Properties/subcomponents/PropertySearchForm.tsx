import React, { ChangeEvent, FunctionComponent } from "react";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

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
      <Form onSubmit={(e) => handleSubmit(e)}>
        <Form.Group controlId="search-query">
          <Form.Label>Search Query</Form.Label>
          <Form.Control
            type="text"
            id="search-query"
            value={searchQuery}
            onChange={handleSearchQueryChange}
          />
        </Form.Group>
        <Form.Group controlId="search-type">
          <Form.Label>Search Type</Form.Label>
          <Form.Control
            as="select"
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
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="search-method">
          <Form.Label>Search Method</Form.Label>
          <Form.Control
            as="select"
            id="search-method"
            value={searchMethod}
            onChange={handleSearchMethodChange}
          >
            <option value="">None</option>
            <option value="contains">Contains</option>
            <option value="starts_with">Starts With</option>
            <option value="ends_with">Ends With</option>
          </Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit">
          Search
        </Button>
      </Form>
    );
  };

  return renderSearchForm();
};

export default PropertySearchForm;
