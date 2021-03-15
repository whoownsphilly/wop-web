import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

import Table from "react-bootstrap/Table";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";

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
    cartoDbLink,
    cartoDbTableName,
    odbLink,
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
      </>
    );
  };

  const renderOpenDataPhillyTable = () => {
    return (
      <>
        <h1>Open Data Philly Data Reference</h1>
        <ListGroup variant="flush">
          <ListGroup.Item>
            <Button variant="link" href={cartoDbLink}>
              CartoDb Link
            </Button>
          </ListGroup.Item>
          <ListGroup.Item>
            CartoDb Table Name: {cartoDbTableName}
          </ListGroup.Item>
          <ListGroup.Item>
            <Button variant="link" href={odbLink}>
              ODB Link
            </Button>
          </ListGroup.Item>
        </ListGroup>
      </>
    );
  };

  return (
    <>
      {renderMetadataTable()}
      {renderOpenDataPhillyTable()}
    </>
  );
};

const mapStateToProps = (state: RootState) => ({
  metadata: selectPropertyMetadata(state),
});

export default connect(mapStateToProps)(MetadataDisplay);
