/* eslint-disable react/jsx-props-no-spreading */
import React, { FunctionComponent, useMemo } from "react";
import { useTable } from "react-table";

import { Property } from "../types";

interface Props {
  properties: Property[];
}

const PropertyDataTable: FunctionComponent<Props> = (props: Props) => {
  const { properties } = props;

  const tableData = useMemo(() => {
    return properties.map((property) => {
      const UNKNOWN = "unknown";
      const {
        location,
        lat,
        lng,
        mailingAddress1,
        mailingAddress2,
        mailing_care_of: mailingCareOf,
        mailing_city_state: mailingCityState,
        owner_2: owner2,
        unit,
        parcel_number: parcelNumber,
      } = property;

      return {
        location: location || UNKNOWN,
        lat: lat || UNKNOWN,
        lng: lng || UNKNOWN,
        mailingAddress1: mailingAddress1 || UNKNOWN,
        mailingAddress2: mailingAddress2 || UNKNOWN,
        mailingCareOf: mailingCareOf || UNKNOWN,
        mailingCityState: mailingCityState || UNKNOWN,
        owner2: owner2 || UNKNOWN,
        unit: unit || UNKNOWN,
        parcelNumber: parcelNumber || UNKNOWN,
      };
    });
  }, [properties]);

  const columns = useMemo(
    () => [
      {
        Header: "Location",
        accessor: "location",
      },
      {
        Header: "Coordinates",
        columns: [
          {
            Header: "Lat",
            accessor: "lat",
          },
          {
            Header: "Lng",
            accessor: "lng",
          },
        ],
      },
      {
        Header: "Owner Mailing Information",
        columns: [
          {
            Header: "Mailing Address 1",
            accessor: "mailingAddress1",
          },
          {
            Header: "Mailing Address 2",
            accessor: "mailingAddress2",
          },
          {
            Header: "Mailing Care Of",
            accessor: "mailingCareOf",
          },
          {
            Header: "Mailing City, State",
            accessor: "mailingCityState",
          },
        ],
      },
      {
        Header: "Owner 2",
        accessor: "owner2",
      },
      {
        Header: "Parcel Number",
        accessor: "parcelNumber",
      },
      {
        Header: "Unit",
        accessor: "unit",
      },
    ],
    []
  );

  /**
   * Why is this ignored? Well React Table doesn't play nice with TS
   * and I got covid brain right now
   *
   * TODO Fix typing on this one
   */
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
  } = useTable({ columns, data: tableData });

  const renderTableHead = () => {
    return (
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th {...column.getHeaderProps()}>{column.render("Header")}</th>
            ))}
          </tr>
        ))}
      </thead>
    );
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const renderTableData = (cell: any) => {
    return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>;
  };

  const renderTableRow = () => {
    return rows.map((row) => {
      prepareRow(row);

      return (
        <tr {...row.getRowProps()}>
          {row.cells.map((cell) => {
            return renderTableData(cell);
          })}
        </tr>
      );
    });
  };

  const renderTableBody = () => {
    return <tbody {...getTableBodyProps()}>{renderTableRow()}</tbody>;
  };

  const renderTable = () => {
    return (
      <table {...getTableProps()}>
        {renderTableHead()}
        {renderTableBody()}
      </table>
    );
  };

  return (
    <>
      <h1>Property Data Table</h1>
      {renderTable()}
    </>
  );
};

export default PropertyDataTable;
