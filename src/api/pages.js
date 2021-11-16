export const getPropertyPageInfo = (parcel_number, date_since) => {
  const url =
    "api/v1/property/historical_details/?parcel_number=" +
    parcel_number +
    "&date_since=" +
    date_since;
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

export const getOwnerPageInfo = owner_name => {
  const url = "api/v1/owner_page/?owner_name=" + owner_name;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getOwnersCurrentPropertiesMapInfo = parcelNumber => {
  const url =
    "api/v1/owner_current_properties_map/?parcel_number=" + parcelNumber;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};
