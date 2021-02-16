import React, { FunctionComponent, useState } from "react";
import { connect } from "react-redux";
import { Dispatch } from "redux";

import { submitPropertySearchForm as actionSubmitPropertySearchForm } from "./redux/actions";

import { PropertySearchState } from "./types";

import PropertySearchForm from "./subcomponents/PropertySearchForm";
import SearchError from "./subcomponents/SearchError";
import PropertyDataTable from "./subcomponents/PropertyDataTable";

interface DispatchProps {
  submitPropertySearchForm: (
    form: PropertySearchState,
    resolve: () => void,
    reject: (errorMessage: string) => void
  ) => void;
}

type Props = DispatchProps;

const Properties: FunctionComponent<Props> = (props: Props) => {
  const intitialSearchState: PropertySearchState = {
    firstName: "",
    lastName: "",
    searchType: "owner",
    searchMethod: "contains",
  };

  const [searchState, updateSearchState] = useState<PropertySearchState>(
    intitialSearchState
  );
  const [errorState, updateErrorState] = useState<string>("");
  const [showDataTable, setShowDataTable] = useState<boolean>(false);

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const { lastName } = searchState;

    if (!lastName) {
      updateErrorState("Must enter a last name.");
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

  const renderDataTable = () => {
    let dataTable = null;
    if (showDataTable) {
      dataTable = <PropertyDataTable />;
    }

    return dataTable;
  };

  return (
    <>
      <h1>I am the properties page.</h1>
      <hr />
      <PropertySearchForm
        handleSubmit={handleSearchSubmit}
        searchState={searchState}
        updateSearchState={updateSearchState}
      />
      <SearchError errorMessage={errorState} />
      {renderDataTable()}
    </>
  );
};

const mapDispatchToProps = (dispatch: Dispatch) => {
  return {
    submitPropertySearchForm: (
      form: PropertySearchState,
      resolve: () => void,
      reject: (errorMessage: string) => void
    ) => dispatch(actionSubmitPropertySearchForm(form, resolve, reject)),
  };
};

export default connect(null, mapDispatchToProps)(Properties);
