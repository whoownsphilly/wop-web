export const getTableInfo = (tableName, searchType, searchToMatch) => {
  const url =
    process.env.VUE_APP_DJANGO_URL +
    "/api/v1/table/" +
    tableName +
    "/" +
    "?search_to_match=" +
    searchToMatch +
    "&search_type=" +
    searchType;
  ("&search_method=equals");
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getBioTableInfo = mailingStreet => {
  const url =
    process.env.VUE_APP_DJANGO_URL +
    "/api/v1/bios/?mailing_street=" +
    mailingStreet;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};

export const getOwnersTimelineTableInfo = owner => {
  const url =
    process.env.VUE_APP_DJANGO_URL +
    "/api/v1/owners_timeline/?owner_name=" +
    owner;
  return fetch(url, {
    method: "GET"
  }).then(response => {
    return response.json();
  });
};
