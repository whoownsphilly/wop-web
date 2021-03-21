import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

import Table from "react-bootstrap/Table";

import { selectPropertyMetadata } from "../redux/selectors";
import { RootState } from "../../../Store/RootReducer";

import { PropertyMetadata } from "../types";

interface StateProps {
  metadata: PropertyMetadata;
}

type Props = StateProps;

const MetadataDisplay: FunctionComponent<Props> = (props: Props) => {
  const { metadata } = props;

  const {
    cartoDbTableName,
    searchToMatch,
    searchMethod,
    searchQuery,
    searchType,
    title,
  } = metadata;

  const renderMetadataTable = () => {
    return (
      <>
        <h1>Search Metadata</h1>
        <Table size="sm">
          <thead>
            <tr>
              <th>Metadata Key</th>
              <th>Metadata Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Title</td>
              <td>{title}</td>
            </tr>
            <tr>
              <td>Search to Match</td>
              <td>{searchToMatch}</td>
            </tr>
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
            <tr>
              <td>CartoDb Table Name</td>
              <td>{cartoDbTableName}</td>
            </tr>
          </tbody>
        </Table>
      </>
    );
  };

  return <>{renderMetadataTable()}</>;
};

const mapStateToProps = (state: RootState) => ({
  metadata: selectPropertyMetadata(state),
});

export default connect(mapStateToProps)(MetadataDisplay);
