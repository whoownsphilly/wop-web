import React, { FunctionComponent } from "react";

interface Props {
  errorMessage: string;
}

const SearchError: FunctionComponent<Props> = (props: Props) => {
  const { errorMessage } = props;

  let searchError = null;
  if (errorMessage) {
    searchError = <p>{errorMessage}</p>;
  }

  return searchError;
};

export default SearchError;
