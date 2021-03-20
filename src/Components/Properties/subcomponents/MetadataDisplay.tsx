import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

import { selectPropertyMetadata } from "../redux/selectors";

import { PropertyMetadata } from "../types";

import { RootState } from "../../../Store/RootReducer";

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

  return (
    <>
      <div>
        <p>Title</p>
        <p>{title}</p>
      </div>
      <div>
        <p>Search Type</p>
        <p>{searchType}</p>
      </div>
      <div>
        <p>Search Method</p>
        <p>{searchMethod}</p>
      </div>
      <div>
        <p>Search Query</p>
        <p>{searchQuery}</p>
      </div>
      <div>
        <p>CartoDb Link</p>
        <p>{cartoDbLink}</p>
      </div>
      <div>
        <p>cartoDbTableName</p>
        <p>{cartoDbTableName}</p>
      </div>
      <div>
        <p>odbLink</p>
        <p>{odbLink}</p>
      </div>
    </>
  );
};

const mapStateToProps = (state: RootState) => ({
  metadata: selectPropertyMetadata(state),
});

export default connect(mapStateToProps)(MetadataDisplay);
