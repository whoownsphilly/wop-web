export const getPropertyBasicsPageInfo = (parcel_number, violations_complaints_date_since) => {
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

export const getOwnersCurrentPropertiesMapInfo = parcelNumber => {
  const url =
    "api/v1/owner_current_properties_map/?parcel_number=" + parcelNumber;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};
