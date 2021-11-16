<template>
<div>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader content="Finding All Information for this owner..." />
    </sui-dimmer>
  </div>
  <div v-else>
          <sui-grid>
            <sui-grid-row>
              <sui-grid-column :width="6">
                <property-portfolio :parcelNumber="parcelNumber" />
              </sui-grid-column>
              <sui-grid-column :width="10">
              </sui-grid-column>
            </sui-grid-row>
            <sui-grid-row>
              <sui-grid-column>
              </sui-grid-column>
            </sui-grid-row>
          </sui-grid>
    <h2>connected to {{ nUniqueProperties }} propert<span v-if="nUniqueProperties > 1">ies</span><span v-else>y</span></h2>
    <vue-apex-bar-chart :data="ownerPropertyCountsByName"/>
    <vue-apex-timeline :data="ownerPropertyTimelineData" labelCol="location_unit" startCol="start_dt" endCol="end_dt"/>
    <h2>Property Ownership Timeline</h2>
    <data-table 
        :rows="ownerPropertyTimelineData" 
        :columns="ownerPropertyTimelineDataColumns"
        title="Owner Timeline"
    />
    <h2>Owner's Violation History</h2>
    Placeholder
    <h2>Owner's Complaint History</h2>
    Placeholder

    <leaflet-map v-if="$siteMode.mode !== 'basic'"
      :latLngs="ownerPropertyTimelineData"
    />
    </div>
  </div>
</template>

<script>
import { getOwnerPageInfo } from '@/api/pages';
import VueApexTimeline from '@/components/ui/charts/Timeline';
import VueApexBarChart from '@/components/ui/charts/BarChart';
import LeafletMap from "@/components/ui/LeafletMap";
import DataTable from "@/components/ui/DataTable";

export default {
  name: "HistoricalOwnerTab",
  components: { VueApexTimeline, VueApexBarChart, LeafletMap, DataTable},
  props: {
    ownerName: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      loading: false,
      ownerPropertyTimelineData: [],
      ownerPropertyCountsByName: [],
    };
  },
  computed: {
      nUniqueProperties() { return [...new Set(this.ownerPropertyTimelineData.map(item => item.location_unit))].length || null;},
      ownerPropertyTimelineDataColumns() { 
          if (this.ownerPropertyTimelineData.length > 0){ 
              return Object.keys(this.ownerPropertyTimelineData[0]).map(
                col => {return {label: col, field: col}}
              )
        } else{ 
            return []
        }
    },
  },
  methods: {
      },
  created() {
    this.loading = true 
    // get all time-based data for the last year
    getOwnerPageInfo(this.ownerName).then(ownerResults => {
        this.ownerPropertyTimelineData = ownerResults['owner_property_timeline']; 
        this.loading = false;
        this.ownerPropertyCountsByName = ownerResults['owner_property_counts_by_name']
        console.log(this.ownerPropertyCountsByName)
    })
  },
};
</script>
