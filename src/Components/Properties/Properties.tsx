import React, { FunctionComponent, useState } from "react";
import { connect } from "react-redux";
import { Dispatch } from "redux";

import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";

import { submitPropertySearchForm as actionSubmitPropertySearchForm } from "./redux/actions";
import { selectPropertiesList } from "./redux/selectors";
import { RootState } from "../../Store/RootReducer";

import { Property, PropertySearchState } from "./types";

import PropertySearchForm from "./subcomponents/PropertySearchForm";
import SearchError from "./subcomponents/SearchError";
import PropertyDataTable from "./subcomponents/PropertyDataTable";
import SearchInfoDisplay from "./subcomponents/SearchInfoDisplay";
import MetadataDisplay from "./subcomponents/MetadataDisplay";

import "./styles.css";

interface StateProps {
  properties: Property[];
}

interface DispatchProps {
  submitPropertySearchForm: (
    form: PropertySearchState,
    resolve: () => void,
    reject: (errorMessage: string) => void
  ) => void;
}

type Props = DispatchProps & StateProps;

const Properties: FunctionComponent<Props> = (props: Props) => {
  const intitialSearchState: PropertySearchState = {
    searchQuery: "",
    searchType: "owner",
    searchMethod: "contains",
  };

  const [searchState, updateSearchState] = useState<PropertySearchState>(
    intitialSearchState
  );
  const [errorState, updateErrorState] = useState<string>("");
  const [showDataTable, setShowDataTable] = useState<boolean>(false);
  const [showMetadata, setShowMetadata] = useState<boolean>(false);

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const { searchQuery } = searchState;

    if (!searchQuery) {
      updateErrorState("Must enter a search query/term.");
    } else {
      const { submitPropertySearchForm } = props;

      const resolve = () => {
        setShowDataTable(true);
      };
      const reject = (errorMessage: string) => {
        updateErrorState(errorMessage);
      };

      submitPropertySearchForm(searchState, resolve, reject);
    }
  };

  const renderTableMetadata = () => {
    let buttonText = "Show Metadata";
    let metadataTSX = null;
    if (showMetadata) {
      buttonText = "Hide Metadata";
      metadataTSX = (
        <Container style={{ margin: ".5vw" }}>
          <SearchInfoDisplay />
          <MetadataDisplay />
        </Container>
      );
    }

    return (
      <>
        <Button
          type="button"
          onClick={() => setShowMetadata(!showMetadata)}
          style={{ margin: ".5vw" }}
        >
          {buttonText}
        </Button>
        {metadataTSX}
      </>
    );
  };

  const renderDataTable = () => {
    const { properties } = props;

    let dataTable = null;
    if (showDataTable && properties) {
      dataTable = (
        <Container
          style={{
            border: "1px solid black",
            borderRadius: ".5%",
            padding: "1vw",
          }}
        >
          <h1>Property Data Table</h1>
          {renderTableMetadata()}
          <PropertyDataTable properties={properties} />
        </Container>
      );
    }

    return dataTable;
  };

  return (
    <>
      <h1>I am the properties page.</h1>
      <hr />
      <Container style={{ width: "75%" }}>
        <PropertySearchForm
          handleSubmit={handleSearchSubmit}
          searchState={searchState}
          updateSearchState={updateSearchState}
        />
        <SearchError errorMessage={errorState} />
      </Container>
      <hr />
      {renderDataTable()}
    </>
  );
};

const mapStateToProps = (state: RootState) => ({
  properties: selectPropertiesList(state),
});

const mapDispatchToProps = (dispatch: Dispatch) => {
  return {
    submitPropertySearchForm: (
      form: PropertySearchState,
      resolve: () => void,
      reject: (errorMessage: string) => void
    ) => dispatch(actionSubmitPropertySearchForm(form, resolve, reject)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Properties);
