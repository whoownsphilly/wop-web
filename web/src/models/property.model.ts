import {CurrencyFormatter} from "../services/utility.helper";

export class Property {
    parcelNumber = ""
    violationsComplaintsDateSince = ""
    hasActiveRentalLicense = false
    rentalLicenseExpiration = ""
    latestAssessmentYear = ""
    latestAssessmentMarketValue = ""
    nViolations = 0
    nViolationsOpen = 0
    nViolationsClosedSince = 0
    nComplaintsSince = 0
    nPropertiesOnDeed = 0
    isEstimateOfYearBuilt = false
    yearBuilt = 0
    hasHomesteadExemption = false
    categoryCodeDescription = ""
    buildingCodeDescription = ""
    location = ""

    public static toProperty(propertyResults): Property {
        const property = new Property()
        property.parcelNumber = propertyResults["percent_number"]
        property.hasActiveRentalLicense = propertyResults["has_active_rental_license"]
        property.rentalLicenseExpiration = propertyResults["rental_license_expiration_date"]
        property.latestAssessmentYear = propertyResults["latest_assessment_year"]
        property.latestAssessmentMarketValue =  CurrencyFormatter.USDollar.format(propertyResults["latest_assessment_market_value"])
        property.nViolations = propertyResults["n_violations"]
        property.nViolationsOpen = propertyResults["n_violations_open"]
        property.nViolationsClosedSince = propertyResults["n_violations_closed_since"]
        property.nComplaintsSince = propertyResults["n_complaints_since"]
        property.nPropertiesOnDeed = propertyResults["n_properties_on_deed"]
        property.isEstimateOfYearBuilt = propertyResults["is_estimate_of_year_built"]
        property.yearBuilt = propertyResults["year_built"]
        property.hasHomesteadExemption = propertyResults["has_homestead_exemption"]
        property.categoryCodeDescription = propertyResults["category_code_description"]
        property.buildingCodeDescription = propertyResults["building_code_description"]
        property.location = propertyResults["location"]

        return property
    }
}