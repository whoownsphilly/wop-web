<template>
  <div class="property">
    <div v-if="loading">
      <sui-dimmer active inverted>
        <sui-loader :content="loadingContent" />
      </sui-dimmer>
    </div>
    <div v-else class="dashboard">
      <property-headline
        :propertyString="propertyString"
        :latestOwnerString="latestOwnerString"
        :ownerByMailingAddress="ownerByMailingAddress"
        :propertySourceString="propertySourceString"
      />
      <sui-tab>
        <sui-tab-pane title="Summary">
          <sui-grid>
            <sui-grid-row>
              <sui-grid-column :width="6">
                <div style="height:600px">
                  <vue-iframe :src="streetViewLink" />
                </div>
              </sui-grid-column>
              <sui-grid-column :width="10">
                <property-basics :parcelNumber="parcelNumber" />
                <router-link
                  to="/take-action"
                  class="ui button positive"
                  tag="button"
                  >Click here to take action!</router-link
                >
              </sui-grid-column>
            </sui-grid-row>
          </sui-grid>
        </sui-tab-pane>
        <sui-tab-pane title="Property Details">
          <property-details :parcelNumber="parcelNumber" />
        </sui-tab-pane>
        <sui-tab-pane title="Owner Details">
          <historical-owner-tab
            :ownerName="latestOwnerString"
            :parcelNumber="parcelNumber"
          />
        </sui-tab-pane>
        <sui-tab-pane
          v-if="propertyResult.crowd_sourced"
          title="Crowd-Sourced Details"
        >
          <crowd-sourced-tab
            :bioResults="propertyResult.crowd_sourced.results"
            :mailingStreet="propertyResult.latest_mailing_street"
          />
        </sui-tab-pane>
      </sui-tab>
    </div>
  </div>
</template>

<script>
import CrowdSourcedTab from "@/components/page/crowdSourced";
import PropertyHeadline from "@/components/page/PropertyHeadline";
import PropertyBasics from "@/components/page/property";
import PropertyDetails from "@/components/page/property/PropertyDetails";
import HistoricalOwnerTab from "@/components/page/owner";
import { getPropertyLatestOwnerDetailsInfo } from "@/api/pages";

export default {
  name: "PropertyPage",
  components: {
    CrowdSourcedTab,
    PropertyHeadline,
    PropertyBasics,
    PropertyDetails,
    HistoricalOwnerTab
  },
  data() {
    return {
      loading: false,
      loadingStep: "",
      streetViewLink: null,
      parcelNumber: this.$route.params.parcelNumber,
      propertyResult: null,
      propertySourceString: "based on the latest property assessment.",
      properties: [],
      latestTransaction: null,
      ownerBasedResults: { violations: { rows: [] }, complaints: { rows: [] } },
      latestRentalLicense: null,
      fullOwnersList: [],
      ownerTimelineData: []
    };
  },
  computed: {
    loadingContent() {
      return (
        "Finding all " +
        this.loadingStep +
        " related information (may take some time)..."
      );
    }
  },
  created() {
    this.loading = true;
    // get all time-based data for the last year
    getPropertyLatestOwnerDetailsInfo(this.parcelNumber).then(result => {
      this.propertyResult = result;
      this.propertyString = result["full_address"];
      this.latestOwnerString = result["latest_owner"];
      this.ownerByMailingAddress = result["owner_by_mailing_address"] || null;
      this.propertySourceString = result["owner_is_from_deed"]
        ? "based on the latest deed transfer."
        : "based on the latest property assessment.";
      this.streetViewLink = result["street_view_link"];
      this.loading = false;
    });
  }
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
