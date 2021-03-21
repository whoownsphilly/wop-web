/* eslint-disable @typescript-eslint/no-explicit-any */
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
// eslint-disable-next-line import/prefer-default-export
export const groupColumns = (columns: any): any => {
  const generalIDs = ["location", "unit"];
  const coordinateIDs = ["lat", "lng"];
  const ownerIDs = ["owner1", "owner2"];
  const mailingInformationIDs = [
    "mailingCareOf",
    "mailingAddress1",
    "mailingAddress2",
    "mailingStreet",
    "mailingCityState",
  ];
  const propertyInformationIDs = [
    "parcelNumber",
    "buildingCodeDescription",
    "categoryCodeDescription",
    "homesteadExemption",
    "yearBuilt",
    "yearBuiltEstimate",
  ];
  const propertyLinksIDs = [
    "linkCyclomediaStreetView",
    "linkPropertyPhilaGov",
    "linkAtlas",
    "linkLicenseInspections",
  ];

  const generalGroup: any = [];
  const coordinateGroup: any = [];
  const ownerGroup: any = [];
  const mailingGroup: any = [];
  const propertyInfoGroup: any = [];
  const propertyLinksGroup: any = [];

  columns.forEach((column: any) => {
    const { id } = column;

    if (generalIDs.includes(id)) {
      generalGroup.push(column);
    }
    if (coordinateIDs.includes(id)) {
      coordinateGroup.push(column);
    }
    if (ownerIDs.includes(id)) {
      ownerGroup.push(column);
    }
    if (mailingInformationIDs.includes(id)) {
      mailingGroup.push(column);
    }
    if (propertyInformationIDs.includes(id)) {
      propertyInfoGroup.push(column);
    }
    if (propertyLinksIDs.includes(id)) {
      propertyLinksGroup.push(column);
    }
  });

  return {
    generalGroup,
    coordinateGroup,
    ownerGroup,
    mailingGroup,
    propertyInfoGroup,
    propertyLinksGroup,
  };
};
