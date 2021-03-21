/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react/jsx-props-no-spreading */
import React, {
  forwardRef,
  FunctionComponent,
  useEffect,
  useMemo,
} from "react";
import { useSortBy, useTable } from "react-table";

import Table from "react-bootstrap/Table";

import { Property } from "../types";

import TableLink from "../../Common/Table/TableLink";

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
        unit,
        owner_1: owner1,
        owner_2: owner2,
        mailing_care_of: mailingCareOf,
        mailing_street: mailingStreet,
        mailingAddress1,
        mailingAddress2,
        mailing_city_state: mailingCityState,
        parcel_number: parcelNumber,
        building_code_description: buildingCodeDescription,
        category_code_description: categoryCodeDescription,
        homestead_exemption: homesteadExemption,
        year_built: yearBuilt,
        year_built_estimate: yearBuiltEstimate,
        lat,
        lng,
        link_cyclomedia_street_view: linkCyclomediaStreetView,
        link_property_phila_gov: linkPropertyPhilaGov,
        link_atlas: linkAtlas,
        link_license_inspections: linkLicenseInspections,
      } = property;

      return {
        location: location || UNKNOWN,
        unit: unit || UNKNOWN,
        owner1: owner1 || UNKNOWN,
        owner2: owner2 || UNKNOWN,
        mailingCareOf: mailingCareOf || UNKNOWN,
        mailingStreet: mailingStreet || UNKNOWN,
        mailingAddress1: mailingAddress1 || UNKNOWN,
        mailingAddress2: mailingAddress2 || UNKNOWN,
        mailingCityState: mailingCityState || UNKNOWN,
        parcelNumber: parcelNumber || UNKNOWN,
        buildingCodeDescription: buildingCodeDescription || UNKNOWN,
        categoryCodeDescription: categoryCodeDescription || UNKNOWN,
        homesteadExemption: homesteadExemption || UNKNOWN,
        yearBuilt: yearBuilt || UNKNOWN,
        yearBuiltEstimate: yearBuiltEstimate || UNKNOWN,
        lat: lat || UNKNOWN,
        lng: lng || UNKNOWN,
        linkCyclomediaStreetView: linkCyclomediaStreetView || UNKNOWN,
        linkPropertyPhilaGov: linkPropertyPhilaGov || UNKNOWN,
        linkAtlas: linkAtlas || UNKNOWN,
        linkLicenseInspections: linkLicenseInspections || UNKNOWN,
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
        Header: "Unit",
        accessor: "unit",
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
        Header: "Owner(s)",
        columns: [
          {
            Header: "Owner 1",
            accessor: "owner1",
          },
          {
            Header: "Owner 2",
            accessor: "owner2",
          },
        ],
      },
      {
        Header: "Owner Mailing Information",
        columns: [
          {
            Header: "Mailing Care Of",
            accessor: "mailingCareOf",
          },
          {
            Header: "Mailing Address 1",
            accessor: "mailingAddress1",
          },
          {
            Header: "Mailing Address 2",
            accessor: "mailingAddress2",
          },
          {
            Header: "Mailing Street",
            accessor: "mailingStreet",
          },
          {
            Header: "Mailing City, State",
            accessor: "mailingCityState",
          },
        ],
      },
      {
        Header: "Property Information",
        columns: [
          {
            Header: "Parcel Number",
            accessor: "parcelNumber",
          },
          {
            Header: "Building Code Description",
            accessor: "buildingCodeDescription",
          },
          {
            Header: "Category Code Description",
            accessor: "categoryCodeDescription",
          },
          {
            Header: "Homestead Exemption",
            accessor: "homesteadExemption",
          },
          {
            Header: "Year Built",
            accessor: "yearBuilt",
          },
          {
            Header: "Year Built Estimate",
            accessor: "yearBuiltEstimate",
          },
        ],
      },
      {
        Header: "Property Links",
        columns: [
          {
            Header: "Cyclomedia Street View",
            accessor: "linkCyclomediaStreetView",
            Cell: ({ value }: { value: string }) => (
              <TableLink link={value} linkText="Street View" />
            ),
          },
          {
            Header: "Property Phila Gov",
            accessor: "linkPropertyPhilaGov",
            Cell: ({ value }: { value: string }) => (
              <TableLink link={value} linkText="Property Phila Gov" />
            ),
          },
          {
            Header: "Atlas",
            accessor: "linkAtlas",
            Cell: ({ value }: { value: string }) => (
              <TableLink link={value} linkText="Atlas" />
            ),
          },
          {
            Header: "License & Inspections",
            accessor: "linkLicenseInspections",
            Cell: ({ value }: { value: string }) => (
              <TableLink link={value} linkText="License & Inspections" />
            ),
          },
        ],
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
    allColumns,
    getToggleHideAllColumnsProps,
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
  } = useTable({ columns, data: tableData }, useSortBy);

  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  const renderSortingHeaders = (column) => {
    const { isSorted, isSortedDesc } = column;

    let sortingDisplay = "";
    if (isSorted) {
      sortingDisplay = " 🔼";
      if (isSortedDesc) {
        sortingDisplay = " 🔽";
      }
    }

    return sortingDisplay;
  };

  const renderTableHead = () => {
    return (
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              // eslint-disable-next-line @typescript-eslint/ban-ts-comment
              // @ts-ignore
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                {column.render("Header")}
                <span>{renderSortingHeaders(column)}</span>
              </th>
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

  interface ColumnCheckProps {
    indeterminate?: boolean;
  }

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

  const renderTable = () => {
    return (
      <>
        <div>
          <div>
            <IndeterminateCheckbox {...getToggleHideAllColumnsProps()} /> Toggle
            All
          </div>
          {allColumns.map((column) => (
            <div key={column.id}>
              <label htmlFor="checks">
                <input
                  type="checkbox"
                  id="checks"
                  {...column.getToggleHiddenProps()}
                />{" "}
                {column.id}
              </label>
            </div>
          ))}
          <br />
        </div>
        <Table
          {...getTableProps()}
          responsive
          bordered
          hover
          style={{ height: "30vw" }}
        >
          {renderTableHead()}
          {renderTableBody()}
        </Table>
      </>
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
