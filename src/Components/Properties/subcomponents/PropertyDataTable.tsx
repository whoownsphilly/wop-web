/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable react/no-unused-prop-types */
import React, { FunctionComponent } from "react";
import { connect } from "react-redux";

import {
  selectOwnerFirstName,
  selectOwnerLastName,
  selectPropertiesList,
  selectSearchType,
} from "../redux/selectors";

import { APISearchType, APISearchMethod } from "../../../Utilities/types";
import { Property } from "../types";

import { RootState } from "../../../Store/RootReducer";

interface StateProps {
  firstName: string;
  lastName: string;
  searchType: APISearchType;
  searchMethod: APISearchMethod;
  data: Property[];
}

const PropertyDataTable: FunctionComponent = () => {
  return <p>Property Data Table</p>;
};

const mapStateToProps = (state: RootState) => {
  return {
    firstName: selectOwnerFirstName(state),
    lastName: selectOwnerLastName(state),
    searchType: selectSearchType(state),
    data: selectPropertiesList(state),
  };
};

export default connect(mapStateToProps, null)(PropertyDataTable);
