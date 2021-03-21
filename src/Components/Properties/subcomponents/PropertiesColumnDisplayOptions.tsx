/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react/jsx-props-no-spreading */
import React, { forwardRef, FunctionComponent, useEffect } from "react";
import Container from "react-bootstrap/Container";
import ListGroup from "react-bootstrap/ListGroup";
import Form from "react-bootstrap/Form";

import { groupColumns } from "../propertiesHelpers";

interface ColumnCheckProps {
  indeterminate?: boolean;
}

interface Props {
  getToggleHideAllColumnsProps: any;
  allColumns: any;
}

const PropertiesColumnDisplayOptions: FunctionComponent<Props> = (
  props: Props
) => {
  const { getToggleHideAllColumnsProps, allColumns } = props;

  const useCombinedRefs = (...refs: any): React.MutableRefObject<any> => {
    const targetRef = React.useRef();

    React.useEffect(() => {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      refs.forEach((ref) => {
        if (!ref) return;

        if (typeof ref === "function") {
          ref(targetRef.current);
        } else {
          // eslint-disable-next-line no-param-reassign
          ref.current = targetRef.current;
        }
      });
    }, [refs]);

    return targetRef;
  };

  const IndeterminateCheckbox = forwardRef<HTMLInputElement, ColumnCheckProps>(
    // eslint-disable-next-line react/prop-types
    ({ indeterminate, ...rest }, ref: React.Ref<HTMLInputElement>) => {
      const defaultRef = React.useRef(null);
      const combinedRef = useCombinedRefs(ref, defaultRef);

      useEffect(() => {
        if (combinedRef?.current) {
          combinedRef.current.indeterminate = indeterminate ?? false;
        }
      }, [combinedRef, indeterminate]);

      return (
        <>
          <input type="checkbox" ref={combinedRef} {...rest} />
        </>
      );
    }
  );

  // Commented out as it breaks my styling
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const renderToggleAll = () => {
    return (
      <div>
        <IndeterminateCheckbox {...getToggleHideAllColumnsProps()} />
        Toggle All
      </div>
    );
  };

  const renderOptionsList = (group: any, title: string) => {
    return (
      <Container style={{ width: "20vw", margin: ".5vw" }}>
        <h4>{title}</h4>
        <ListGroup>
          {group.map((column: any) => (
            <ListGroup.Item key={column.id}>
              <Form.Check
                type="checkbox"
                id={column.Header}
                label={column.Header}
                {...column.getToggleHiddenProps()}
              />
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Container>
    );
  };

  const renderColumnToggles = () => {
    const {
      generalGroup,
      coordinateGroup,
      ownerGroup,
      mailingGroup,
      propertyInfoGroup,
      propertyLinksGroup,
    } = groupColumns(allColumns);

    const generalOptionsTSX = renderOptionsList(generalGroup, "General");
    const coordinatesOptionsTSX = renderOptionsList(
      coordinateGroup,
      "Coordinates"
    );
    const OwnerOptionsTSX = renderOptionsList(ownerGroup, "Owner Information");
    const MailingOptionsTSX = renderOptionsList(
      mailingGroup,
      "Owner Mailing Information"
    );
    const PropertyInfoOptionsTSX = renderOptionsList(
      propertyInfoGroup,
      "Property Information"
    );
    const propertyLinkOptionsTSX = renderOptionsList(
      propertyLinksGroup,
      "Property Link Options"
    );

    return (
      <Container style={{ display: "flex", flexWrap: "wrap" }}>
        <Container style={{ display: "flex" }}>
          {generalOptionsTSX}
          {coordinatesOptionsTSX}
          {OwnerOptionsTSX}
        </Container>
        <Container style={{ display: "flex" }}>
          {MailingOptionsTSX}
          {PropertyInfoOptionsTSX}
          {propertyLinkOptionsTSX}
        </Container>
      </Container>
    );
  };

  return (
    <Container style={{ border: "1px solid black" }}>
      {/* {renderToggleAll()} */}
      {renderColumnToggles()}
    </Container>
  );
};

export default PropertiesColumnDisplayOptions;
