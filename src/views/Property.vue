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
                <property-portfolio :parcelNumber="parcelNumber"/>
              </sui-grid-column>
              <sui-grid-column :width="10">
                <property-results :parcelNumber="parcelNumber"/>
                  <router-link
                    to="/info"
                    class="ui button positive"
                    tag="button"
                    >Click to take action!</router-link
                  >
              </sui-grid-column>
            </sui-grid-row>
            <sui-grid-row>
              <sui-grid-column>
              <sui-divider horizontal
                >Crowd-Sourced Owner Information</sui-divider
              >
                <historical-mailing-address-tab v-if="propertyResult.crowd_sourced" :bioResults="propertyResult.crowd_sourced.results" :mailingStreet="propertyResult.latest_mailing_street"/>
              </sui-grid-column>
            </sui-grid-row>
          </sui-grid>
        </sui-tab-pane>
        <sui-tab-pane title="Property Details">
          <historical-property-tab :parcelNumber="parcelNumber" />
        </sui-tab-pane>
        <sui-tab-pane
          title="Owner Details"
        >
          <historical-owner-tab
            :ownerName="latestOwnerString"
          />
        </sui-tab-pane>
      </sui-tab>
    </div>
  </div>
</template>

<script>
import HistoricalPropertyTab from "@/components/page/property";
import HistoricalOwnerTab from "@/components/page/owner";
import HistoricalMailingAddressTab from "@/components/page/mailing_address";
import PropertyHeadline from "@/components/page/property/PropertyHeadline";
import PropertyResults from "@/components/page/property";
import PropertyPortfolio from "@/components/page/property/Portfolio";
import { getPropertyLatestOwnerDetailsInfo } from '@/api/pages';

export default {
  name: "Property",
  components: {
    PropertyHeadline,
    HistoricalPropertyTab,
    HistoricalOwnerTab,
    HistoricalMailingAddressTab,
    PropertyPortfolio,
    PropertyResults
  },
  data() {
    return {
      loading: false,
      loadingStep: "",
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
    },
  },
  created() {
    this.loading = true 
    // get all time-based data for the last year
    getPropertyLatestOwnerDetailsInfo(this.parcelNumber).then(result => {
        this.propertyResult = result
        this.propertyString = result['address']
        this.latestOwnerString = result['latest_owner']
        this.ownerByMailingAddress = result['owner_by_mailing_address'] || null
        this.propertySourceString = result['owner_is_from_deed'] ? "based on the latest deed transfer." : "based on the latest property assessment."
        this.loading = false
    })
  },
}
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
