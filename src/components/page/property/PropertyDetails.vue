<template>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader content="Finding All Information for this property..." />
    </sui-dimmer>
  </div>
  <div v-else>
    <h2>Who owned this property since 2000?</h2>
    <vue-apex-timeline :data="propertyOwnershipTimelineData" labelCol="owner" />
    <vue-apex-line-chart :data="propertyValueTimelineData" />
  </div>
</template>

<script>
import { getPropertyDetailsPageInfo } from "@/api/pages";
import VueApexTimeline from "@/components/ui/charts/Timeline";
import VueApexLineChart from "@/components/ui/charts/LineChart";

export default {
  name: "PropertyInfo",
  components: { VueApexTimeline, VueApexLineChart },
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
      loading: false
    };
  },
  created() {
    this.loading = true;
    // get all time-based data for the last year
    getPropertyDetailsPageInfo(this.parcelNumber).then(propertyResults => {
      this.propertyOwnershipTimelineData =
        propertyResults["property_ownership_timeline"];
      this.propertyValueTimelineData =
        propertyResults["property_value_timeline"];
      this.loading = false;
    });
  }
};
</script>
