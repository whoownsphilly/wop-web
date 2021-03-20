import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

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

  return (
    <>
      <div>
        <p>Search Query</p>
        <p>{searchQuery}</p>
      </div>
      <div>
        <p>Search Type</p>
        <p>{searchType}</p>
      </div>
      <div>
        <p>Search Method</p>
        <p>{searchMethod}</p>
      </div>
    </>
  );
};

const mapStateToProps = (state: RootState) => ({
  searchQuery: selectSearchQuery(state),
  searchType: selectSearchType(state),
  searchMethod: selectSearchMethod(state),
});

export default connect(mapStateToProps)(SearchInfoDisplay);
