import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

import Table from "react-bootstrap/Table";

import {
  selectSearchQuery,
  selectSearchMethod,
  selectSearchType,
} from "../redux/selectors";
import { RootState } from "../../../Store/RootReducer";

import { APISearchType, APISearchMethod } from "../../../Utilities/types";

interface StateProps {
  searchQuery: string;
  searchType: APISearchType;
  searchMethod: APISearchMethod;
}

type Props = StateProps;

const SearchInfoDisplay: FunctionComponent<Props> = (props: Props) => {
  const { searchQuery, searchType, searchMethod } = props;

  const renderTable = () => {
    return (
      <Table size="sm">
        <thead>
          <tr>
            <th>Search Option</th>
            <th>Search Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Search Query</td>
            <td>{searchQuery}</td>
          </tr>
          <tr>
            <td>Search Type</td>
            <td>{searchType}</td>
          </tr>
          <tr>
            <td>Search Method</td>
            <td>{searchMethod}</td>
          </tr>
        </tbody>
      </Table>
    );
  };

  return (
    <>
      <h1>Submitted Search Parameters</h1>
      {renderTable()}
    </>
  );
};

const mapStateToProps = (state: RootState) => ({
  searchQuery: selectSearchQuery(state),
  searchType: selectSearchType(state),
  searchMethod: selectSearchMethod(state),
});

export default connect(mapStateToProps)(SearchInfoDisplay);
