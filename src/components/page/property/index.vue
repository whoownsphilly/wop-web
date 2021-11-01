<template>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader content="Finding All Information for this property..." />
    </sui-dimmer>
  </div>
  <div v-else>
  <sui-statistics-group horizontal >
        <sui-statistic in-group v-if="hasActiveRentalLicense" color="green">
          <sui-statistic-value>Does</sui-statistic-value>
          <sui-statistic-label>have an active rental license (expires on {{ rentalLicenseExpiration| luxon }})</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group v-else-if="hasHomesteadExemption">
          <sui-statistic-value>Does not</sui-statistic-value>
          <sui-statistic-label>have an active rental license but has a homestead exemption (might not be a rental?)</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group v-else color="red">
          <sui-statistic-value>Does not</sui-statistic-value>
          <sui-statistic-label>have an active rental license and also no homestead exemption</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group >
          <sui-statistic-value>{{ categoryCodeDescription }}</sui-statistic-value>
          <sui-statistic-label>{{ buildingCodeDescription }}</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group >
          <sui-statistic-value>{{ latestAssessmentMarketValue }}</sui-statistic-value>
          <sui-statistic-label>property value estimate for {{ latestAssessmentYear }}</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group v-if="nViolationsOpen">
          <sui-statistic-value>{{ nViolationsOpen }}</sui-statistic-value>
          <sui-statistic-label>Currently Open Violations</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group v-if="nViolationsSerious">
          <sui-statistic-value>{{ nViolationsSerious }}</sui-statistic-value>
          <sui-statistic-label>Serious Violations since {{ dateSince | luxon }}</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group v-if="nComplaints">
          <sui-statistic-value>{{ nComplaints }}</sui-statistic-value>
          <sui-statistic-label>Complaints {{ dateSince | luxon }}</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group v-if="nPropertiesOnDeed > 1">
          <sui-statistic-value>{{ nPropertiesOnDeed }}</sui-statistic-value>
          <sui-statistic-label>Properties on this deed</sui-statistic-label>
        </sui-statistic>
        <sui-statistic in-group>
          <sui-statistic-value>{{ yearBuilt }}</sui-statistic-value>
          <sui-statistic-label v-if="isEstimateOfYearBuilt">is a rough built year estimate</sui-statistic-label>
          <sui-statistic-label v-else>is the year this was built</sui-statistic-label>
        </sui-statistic>
  </sui-statistics-group>
  <h2>Who owned this property since 2000?</h2>
  <vue-apex-timeline :data="propertyOwnershipTimelineData" labelCol="owner"/>
  <vue-apex-line-chart :data="propertyValueTimelineData"/>
  </div>
</template>

<script>

import { getPropertyPageInfo } from '@/api/pages'; 
import VueApexTimeline from '@/components/ui/Timeline';
import VueApexLineChart from '@/components/ui/LineChart';
import { formatCurrencyValue } from '@/components/utils/formatting.js';

export default {
  name: "PropertyInfo",
  components: { VueApexTimeline, VueApexLineChart},
  props: {
    parcelNumber: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      propertyOwnershipTimelineData: [],
      propertyValueTimelineData: [],
      propertyResults: null,
      hasActiveRentalLicense: null,
      rentalLicenseExperiation: null,
      latestAssessmentMarketValue: null,
      latestAssessmentYear: null,
      nViolationsOpen: null,
      nViolationsSerious: null,
      nComplaints: null,
      nPropertiesOnDeed: null,
      yearBuilt: null,
      isEstimateOfyearBuilt: null,
      hasHomesteadExemption: null,
      buildingCodeDescription: null,
      categoryCodeDescription: null,
      loading: false,
      dateSince: (new Date(new Date().setFullYear(new Date().getFullYear() - 1))).toISOString()
    };
  },
  created() { 
        this.loading = true 
        // get all time-based data for the last year
        getPropertyPageInfo(this.parcelNumber, this.dateSince).then(propertyResults => {
        this.propertyOwnershipTimelineData = propertyResults['property_ownership_timeline']
        this.propertyValueTimelineData = propertyResults['property_value_timeline']
        this.hasActiveRentalLicense = propertyResults['has_active_rental_license']
        this.rentalLicenseExpiration = propertyResults['rental_license_expiration_date']
        this.latestAssessmentYear = propertyResults['latest_assessment_year']
        this.latestAssessmentMarketValue = formatCurrencyValue(propertyResults['latest_assessment_market_value'])
        this.nViolations = propertyResults['n_violations']
        this.nViolationsOpen = propertyResults['n_violations_open']
        this.nViolationsSerious = propertyResults['n_violations_serious']
        this.nComplaints = propertyResults['n_complaints']
        this.nPropertiesOnDeed = propertyResults['n_properties_on_deed']
        this.isEstimateOfYearBuilt = propertyResults['is_estimate_of_year_built']
        this.yearBuilt = propertyResults['year_built']
        this.hasHomesteadExemption = propertyResults['has_homestead_exemption']
        this.categoryCodeDescription = propertyResults['category_code_description']
        this.buildingCodeDescription = propertyResults['building_code_description']
        this.loading = false
  })
      },
  methods: {
    formatCurrencyValue(totalValue) {
      var formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      });
      return formatter.format(totalValue).slice(0, -3);
    },
}
};
</script>
