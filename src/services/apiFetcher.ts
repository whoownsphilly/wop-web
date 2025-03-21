const domain = import.meta.env.PUBLIC_API_DOMAIN || 'https://api.whoownsphilly.org/'
export const getPropertyBasicsPageInfo = (
  parcel_number,
  violations_complaints_date_since: Date
) => {
  const dateFormatter = Intl.DateTimeFormat('sv-SE')
  const url = `${domain}api/v1/property/basics/?parcel_number=${parcel_number}&violations_complaints_date_since=${dateFormatter.format(violations_complaints_date_since)}`
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}

export const getPropertyDetailsPageInfo = (parcel_number) => {
  const url = `${domain}api/v1/property/details/?parcel_number=${parcel_number}`
  // const url = "api/v1/property/details/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}

export const getPropertyLatestOwnerDetailsInfo = (parcel_number) => {
  const url = `${domain}api/v1/property/latest_owner_details/?parcel_number=${parcel_number}`
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}

export const getOwnerPageInfoByName = (parcel_number) => {
  const url = `${domain}api/v1/owner/by_name/?parcel_number=${parcel_number}`
  // const url = "api/v1/owner/by_name/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}

export const getOwnerPageInfoByMailingAddress = (parcel_number) => {
  const url = `${domain}api/v1/owner/by_mailing_address/?parcel_number=${parcel_number}`
  // const url = "api/v1/owner/by_mailing_address/?parcel_number=" + parcel_number;
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}

export const getCrowdSourcedPageInfo = (parcelNumber) => {
  const url = `${domain}api/v1/crowd_sourced/?parcel_number=${parcelNumber}`
  // const url = "api/v1/crowd_sourced/?parcel_number=" + parcelNumber;
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}

export const getNeighborhoodsPageInfo = (
  bounds,
  zipCode,
  addressDistance,
  latitude,
  longitude,
  searchBy,
  licenseFilter,
  condoFilter,
  ownerOccupiedFilter,
  numUnitsPerList,
  numLists,
  buildingTypes,
  rentalBuildingTypes
) => {
  const url =
    `${domain}api/v1/neighborhoods/` +
    '?northeast_lat=' +
    bounds._northEast.lat +
    '&northeast_lng=' +
    bounds._northEast.lng +
    '&southwest_lat=' +
    bounds._southWest.lat +
    '&southwest_lng=' +
    bounds._southWest.lng +
    '&search_by=' +
    searchBy +
    '&license_filter=' +
    licenseFilter +
    '&condo_filter=' +
    condoFilter +
    '&owner_occupied_filter=' +
    ownerOccupiedFilter +
    '&num_units_per_list=' +
    numUnitsPerList +
    '&num_lists=' +
    numLists +
    '&building_types=' +
    buildingTypes +
    '&rental_building_types=' +
    rentalBuildingTypes +
    '&starting_latitude=' +
    latitude +
    '&starting_longitude=' +
    longitude +
    '&address_distance=' +
    addressDistance +
    '&zip_code=' +
    zipCode

  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })

  // return fetch(url, {
  //     method: "GET"
  // }).then(response => {
  //     console.log(response)
  //     if (response.ok === false) {
  //         return { status: "error" };
  //     } else {
  //         return response.json();
  //     }
  // });
}

export const getNeighborhoodsPageFromParcelNumbers = (parcelList) => {
  let params = new URLSearchParams(parcelList).toString()
  const url = 'api/v1/neighborhoods_by_parcel_lists/?' + params
  return fetch(url, {
    method: 'GET',
  }).then((response) => {
    return response.json()
  })
}
