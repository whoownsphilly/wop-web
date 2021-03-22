import React, { FunctionComponent } from "react";
import Button from "react-bootstrap/Button";

interface Props {
  link: string;
  linkText: string;
}

const TableLink: FunctionComponent<Props> = (props: Props) => {
  const { link, linkText } = props;

  const escapedLink = link.replace(" ", "%20");

  return (
    <Button variant="link" href={escapedLink} target="_blank">
      {linkText}
    </Button>
  );
};

export default TableLink;
