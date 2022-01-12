<template>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader content="Finding All Information for this property..." />
    </sui-dimmer>
  </div>
  <div v-else>
    <sui-statistics-group horizontal>
      <sui-statistic in-group v-if="hasActiveRentalLicense" color="green">
        <sui-statistic-value>Does</sui-statistic-value>
        <sui-statistic-label
          >have an active rental license (expires on
          {{ rentalLicenseExpiration | luxon }})</sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group v-else-if="hasHomesteadExemption">
        <sui-statistic-value>Does not</sui-statistic-value>
        <sui-statistic-label
          >have an active rental license but has a homestead exemption (this
          property might not be a rental)</sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group v-else color="red">
        <sui-statistic-value>Does not</sui-statistic-value>
        <sui-statistic-label
          >have an active rental license and also no homestead
          exemption</sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>{{ categoryCodeDescription }}</sui-statistic-value>
        <sui-statistic-label>{{ buildingCodeDescription }}</sui-statistic-label>
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>{{
          latestAssessmentMarketValue
        }}</sui-statistic-value>
        <sui-statistic-label
          >property value estimate for
          {{ latestAssessmentYear }}</sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group v-if="nPropertiesOnDeed > 1">
        <sui-statistic-value>{{ nPropertiesOnDeed }}</sui-statistic-value>
        <sui-statistic-label>Properties on this deed</sui-statistic-label>
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>{{ yearBuilt }}</sui-statistic-value>
        <sui-statistic-label v-if="isEstimateOfYearBuilt"
          >is a rough estimate of the year this was built</sui-statistic-label
        >
        <sui-statistic-label v-else
          >is the year this was built</sui-statistic-label
        >
      </sui-statistic>

      <sui-statistic in-group>
        <sui-statistic-value>
          {{ nViolationsOpen || 0 }}
        </sui-statistic-value>
        <sui-statistic-label>currently open violations</sui-statistic-label>
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>
          {{ nViolationsClosedSince || 0 }}
        </sui-statistic-value>
        <sui-statistic-label
          >closed violations since
          {{ violationsComplaintsDateSince | luxon }}</sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>
          {{ nComplaintsSince || 0 }}
        </sui-statistic-value>
        <sui-statistic-label
          >complaints to 311 since
          {{ violationsComplaintsDateSince | luxon }}</sui-statistic-label
        >
      </sui-statistic>
    </sui-statistics-group>
  </div>
</template>

<script>
import { getPropertyBasicsPageInfo } from "@/api/pages";
import { formatCurrencyValue } from "@/components/utils/formatting.js";

export default {
  name: "PropertyInfo",
  components: {},
  props: {
    parcelNumber: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      propertyResults: null,
      streetViewLink: null,
      hasActiveRentalLicense: null,
      rentalLicenseExperiation: null,
      latestAssessmentMarketValue: null,
      latestAssessmentYear: null,
      nViolationsOpen: null,
      nViolationsClosedSince: null,
      nComplaintsSince: null,
      nPropertiesOnDeed: null,
      yearBuilt: null,
      isEstimateOfyearBuilt: null,
      hasHomesteadExemption: null,
      buildingCodeDescription: null,
      categoryCodeDescription: null,
      loading: false,
      violationsComplaintsDateSince: "2007-01-01" //violations data starts in 2007
    };
  },
  created() {
    this.loading = true;
    getPropertyBasicsPageInfo(
      this.parcelNumber,
      this.violationsComplaintsDateSince
    ).then(propertyResults => {
      this.hasActiveRentalLicense =
        propertyResults["has_active_rental_license"];
      this.rentalLicenseExpiration =
        propertyResults["rental_license_expiration_date"];
      this.latestAssessmentYear = propertyResults["latest_assessment_year"];
      this.latestAssessmentMarketValue = formatCurrencyValue(
        propertyResults["latest_assessment_market_value"]
      );
      this.nViolations = propertyResults["n_violations"];
      this.nViolationsOpen = propertyResults["n_violations_open"];
      this.nViolationsClosedSince =
        propertyResults["n_violations_closed_since"];
      this.nComplaintsSince = propertyResults["n_complaints_since"];
      this.nPropertiesOnDeed = propertyResults["n_properties_on_deed"];
      this.isEstimateOfYearBuilt = propertyResults["is_estimate_of_year_built"];
      this.yearBuilt = propertyResults["year_built"];
      this.hasHomesteadExemption = propertyResults["has_homestead_exemption"];
      this.categoryCodeDescription =
        propertyResults["category_code_description"];
      this.buildingCodeDescription =
        propertyResults["building_code_description"];
      this.streetViewLink = propertyResults["street_view_link"];
      this.loading = false;
    });
  },
  methods: {
    formatCurrencyValue(totalValue) {
      var formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      });
      return formatter.format(totalValue).slice(0, -3);
    }
  }
};
</script>
<style>
.ui.accordion .title:not(.ui) {
  font-size: 2em;
}
</style>
