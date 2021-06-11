<template>
  <div class="property">
    <div v-if="result">
    <sui-container text>
        <h2 is="sui-header">{{ result.location }} {{result.unit }}</h2>
        <h2 is="sui-header">Building Description</h2>
        <p>{{ buildingDescription }}</p>

    <h2 is="sui-header">Links</h2>
      <a :href="result.link_atlas" target="_blank">Link to Atlas</a>,
      <a :href="result.link_cyclomedia_street_view" target="_blank">Link to Cyclomedia Street View</a>,
      <a :href="result.link_property_phila_gov" target="_blank">Link to property.phila.gov</a>,
      <a :href="result.link_license_inspections" target="_blank">Link to li.phila.gov</a>
    <h2 v-for="owner in owners" :key="owner">Owner: {{ owner }}</h2>
    </sui-container>
       <sui-tab>
      <sui-tab-pane title="Historical Property Info">
        <historical-property-tab :parcelNumber="this.parcelNumber"/>
      </sui-tab-pane>
      <sui-tab-pane v-for="owner in owners" :key="owner" :title="owner">
        <historical-owner-tab :owner="owner"/>
      </sui-tab-pane>
      <sui-tab-pane title="Crowd-Sourced Info">
        <historical-crowd-sourced-tab :mailingStreet="mailingStreetOrLocation"/>
      </sui-tab-pane>
    </sui-tab>
    </div>
  </div>
</template>

<script>
import HistoricalPropertyTab from '@/components/HistoricalPropertyTab'
import HistoricalOwnerTab from '@/components/HistoricalOwnerTab'
import HistoricalCrowdSourcedTab from '@/components/HistoricalCrowdSourcedTab'
import { getTableInfo } from '@/api/singleTable'

export default {
  name: "Property",
  components: {
      HistoricalPropertyTab,
      HistoricalOwnerTab,
      HistoricalCrowdSourcedTab,
},
  data() {
    return {
      parcelNumber: this.$route.params.parcelNumber,
      result: null,
      resultLoaded: false
    };
  },
  computed: {
    mailingStreetOrLocation() {
        if (this.result !== null) {
            return this.result.mailing_street || this.result.location
        }
        return ''
    },
    owners() {
      const ownerList = [];
      if (this.result !== null) {
        if (this.result.owner_1) {
          ownerList.push(this.result.owner_1);
        }
        if (this.result.owner_2) {
          ownerList.push(this.result.owner_2);
        }
      }
      return ownerList;
    },
    buildingDescription() {
        let year_built_estimate_str = ""
        if(this.result.year_built_estimate === "Y"){
            year_built_estimate_str = " (although this is an estimate)"
        }
        if (this.result !== null){
            return "This building was constructed in " + this.result.year_built +
            year_built_estimate_str +
            ", and is described as a " + this.result.category_code_description +
            ", " +  this.result.building_code_description
        }
        return ''
    }
  },
  created() {
    getTableInfo('properties', 'parcel_number', this.parcelNumber)
    .then(data => {
        if ("results" in data && data.results.rows.length == 1) {
          this.result = data.results.rows[0];
          this.address = this.result.location;
        }
      });
  }
};
</script>
