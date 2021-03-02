import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

import {
  selectOwnerFirstName,
  selectOwnerLastName,
  selectSearchMethod,
  selectSearchType,
} from "../redux/selectors";
import { RootState } from "../../../Store/RootReducer";

import { APISearchType, APISearchMethod } from "../../../Utilities/types";

interface StateProps {
  firstName: string;
  lastName: string;
  searchType: APISearchType;
  searchMethod: APISearchMethod;
}

type Props = StateProps;

const SearchInfoDisplay: FunctionComponent<Props> = (props: Props) => {
  const { firstName, lastName, searchType, searchMethod } = props;

  return (
    <>
      <div>
        <p>Owner Name</p>
        <p>
          {firstName} {lastName}
        </p>
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
  firstName: selectOwnerFirstName(state),
  lastName: selectOwnerLastName(state),
  searchType: selectSearchType(state),
  searchMethod: selectSearchMethod(state),
});

export default connect(mapStateToProps)(SearchInfoDisplay);
