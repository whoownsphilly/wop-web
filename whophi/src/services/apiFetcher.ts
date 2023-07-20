import {Property} from "../models/property.model";
export class ApiFetcher {
    domain = "http://localhost:8081/"
    fetcher: any

    constructor(fetch) {
        this.fetcher = fetch
    }
    getPropertyBasicsPageInfo = async  (
        parcel_number,
        violations_complaints_date_since = '2007-01-01'
    ) => {
        const url = `${this.domain}api/v1/property/basics/?parcel_number=${parcel_number}&violations_complaints_date_since=${violations_complaints_date_since}`
        const response = await this.fetcher(url, { method: "GET" })
        console.log(response)
        const json = await response.json()
        console.log(json)
        return Property.toProperty(json)
    };

    getPropertyDetailsPageInfo = parcel_number => {
        const url = "api/v1/property/details/?parcel_number=" + parcel_number;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            return response.json();
        });
    };

    getPropertyLatestOwnerDetailsInfo = parcel_number => {
        const url =
            "api/v1/property/latest_owner_details/?parcel_number=" + parcel_number;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            return response.json();
        });
    };

    getOwnerPageInfoByName = parcel_number => {
        const url = "api/v1/owner/by_name/?parcel_number=" + parcel_number;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            return response.json();
        });
    };

    getOwnerPageInfoByMailingAddress = parcel_number => {
        const url = "api/v1/owner/by_mailing_address/?parcel_number=" + parcel_number;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            return response.json();
        });
    };

    getCrowdSourcedPageInfo = parcelNumber => {
        const url = "api/v1/crowd_sourced/?parcel_number=" + parcelNumber;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            return response.json();
        });
    };

    getNeighborhoodsPageInfo = (
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
            "&license_filter=" +
            licenseFilter +
            "&condo_filter=" +
            condoFilter +
            "&owner_occupied_filter=" +
            ownerOccupiedFilter +
            "&num_units_per_list=" +
            numUnitsPerList +
            "&num_lists=" +
            numLists +
            "&building_types=" +
            buildingTypes +
            "&rental_building_types=" +
            rentalBuildingTypes +
            "&starting_latitude=" +
            latitude +
            "&starting_longitude=" +
            longitude +
            "&address_distance=" +
            addressDistance +
            "&zip_code=" +
            zipCode;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            if (response.ok === false) {
                return { status: "error" };
            } else {
                return response.json();
            }
        });
    };

    getNeighborhoodsPageFromParcelNumbers = parcelList => {
        let params = new URLSearchParams(parcelList).toString();
        const url = "api/v1/neighborhoods_by_parcel_lists/?" + params;
        return fetch(url, {
            method: "GET"
        }).then(response => {
            return response.json();
        });
    };

}