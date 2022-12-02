export const getPropertyBasicsPageInfo = (
  parcel_number,
  violations_complaints_date_since
) => {
  const url = `api/v1/property/basics/?parcel_number=${parcel_number}&violations_complaints_date_since=${violations_complaints_date_since}`;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getPropertyDetailsPageInfo = parcel_number => {
  const url = "api/v1/property/details/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getPropertyLatestOwnerDetailsInfo = parcel_number => {
  const url =
    "api/v1/property/latest_owner_details/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getOwnerPageInfoByName = parcel_number => {
  const url = "api/v1/owner/by_name/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getOwnerPageInfoByMailingAddress = parcel_number => {
  const url = "api/v1/owner/by_mailing_address/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getCrowdSourcedPageInfo = parcelNumber => {
  const url = "api/v1/crowd_sourced/?parcel_number=" + parcelNumber;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getNeighborhoodsPageInfo = (
  bounds,
  zipCode,
  searchBy,
  filterBy,
  buildingTypes
) => {
  const url =
    "api/v1/neighborhoods/" +
    "?northeast_lat=" +
    bounds._northEast.lat +
    "&northeast_lng=" +
    bounds._northEast.lng +
    "&southwest_lat=" +
    bounds._southWest.lat +
    "&southwest_lng=" +
    bounds._southWest.lng +
    "&search_by=" +
    searchBy +
    "&filter_by=" +
    filterBy +
    "&building_types=" +
    buildingTypes +
    "&zip_code=" +
    zipCode;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getNeighborhoodsPageFromParcelNumbers = parcelList => {
  let params = new URLSearchParams(parcelList).toString();
  const url = "api/v1/neighborhoods_by_parcel_lists/?" + params;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};
