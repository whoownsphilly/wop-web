export class PropertyOwner {
    parcelNumber: 461145600
    yearBuilt: 1915
    yearBuiltIsEstimate: false
    hasHomesteadExemption: true
    location: ""
    lat?: null
    lng?: null
    owner1: ""
    owner2: ""
    mailingStreet: ""
    mailingAddress1: ""
    buildingCodeDescription: ""
    categoryCodeDescription: ""
    nViolationsOpen: 0
    nViolationsClosedSince: 0
    nComplaintsSince: 0
    hasActiveRentalLicense: false
    rentalLicenseExpirationDate: null
    numberOfLicensedRentalUnits: null
    recordingDate: ""
    grantees: ""
    grantors: ""
    cashConsideration: 0
    nPropertiesOnDeed: 1
    latestAssessmentMarketValue: 0
    latestAssessmentYear: 0
    cache: true
    dataKey: 0

    public static ToPropertyOwner(propertyOwnerResults) {
        {\  yearBuilt: 1915
            yearBuiltIsEstimate: false
            hasHomesteadExemption: true
            location: ""
            lat?: null
            lng?: null
            owner1: ""
            owner2: ""
            mailingStreet: ""
            mailingAddress1: ""
            buildingCodeDescription: ""
            categoryCodeDescription: ""
            nViolationsOpen: 0
            nViolationsClosedSince: 0
            nComplaintsSince: 0
            hasActiveRentalLicense: false
            rentalLicenseExpirationDate: null
            this.parcelNumber = propertyOwnerResults["parcel_number"]
            this.yearBuilt = propertyOwnerResults["year_built"]
            this.parcelNumber = propertyOwnerResults["year_built_is_estimate"]
            this.parcelNumber = propertyOwnerResults["has_homestead_exemption"]
            this.parcelNumber = propertyOwnerResults["location"]
            this.parcelNumber = propertyOwnerResults["lat"]
            this.parcelNumber = ropertyOwnerResults["lng"]
            this.parcelNumber = propertyOwnerResults["owner_1"]
            this.parcelNumber = propertyOwnerResults["owner_2"]
            this.parcelNumber = propertyOwnerResults["mailing_street"]
            this.parcelNumber = propertyOwnerResults["mailing_address_1"]
            this.parcelNumber = propertyOwnerResults["building_code_description"]
            this.parcelNumber = propertyOwnerResults["category_code_description"]
            this.parcelNumber = propertyOwnerResults["n_violations_open"]
            this.parcelNumber = propertyOwnerResults["n_violations_closed_since"]
            this.parcelNumber = propertyOwnerResults["n_complaints_since"]
            this.parcelNumber = propertyOwnerResults["has_active_rental_license"]
            this.parcelNumber = propertyOwnerResults["rental_license_expiration_date"]
            this.numberOfLicensedRentalUnits = propertyOwnerResults["number_of_licensed_rental_units"]
            this.recordingDate = propertyOwnerResults["recording_date"]
            this.grantees = propertyOwnerResults["grantees"]
            this.grantors = propertyOwnerResults["grantors"]
            this.cashConsideration = propertyOwnerResults["cash_consideration"]
            this.nPropertiesOnDeed = propertyOwnerResults["n_properties_on_deed"]
            this.latestAssessmentMarketValue = propertyOwnerResults["latest_assessment_market_value"]
            this.latestAssessmentYear = propertyOwnerResults["latest_assessment_year"]
            this.cache = propertyOwnerResults["cache"]
            this.dataKey = propertyOwnerResults["data_key"]
        }
    }
}
