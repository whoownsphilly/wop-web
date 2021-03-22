/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { FunctionComponent } from "react";

interface Props {
  column: any;
}

const TableSortingHeaders: FunctionComponent<Props> = (props: Props) => {
  const { column } = props;
  const { isSorted, isSortedDesc } = column;

  let sortingDisplay = "";
  if (isSorted) {
    sortingDisplay = " 🔼";
    if (isSortedDesc) {
      sortingDisplay = " 🔽";
    }
  }

  return <span>{sortingDisplay}</span>;
};

export default TableSortingHeaders;
