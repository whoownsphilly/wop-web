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
      <div class="ui top attached tabular menu">
        <router-link :to="summaryLink">
          <div class="item" :class="{ active: isActive('property-summary') }">
            Summary
          </div>
        </router-link>
        <router-link :to="propertyDetailsLink">
          <div class="item" :class="{ active: isActive('property-details') }">
            Property Details
          </div>
        </router-link>
        <router-link :to="ownerDetailsLink">
          <div class="item" :class="{ active: isActive('owner') }">
            Owner Details
          </div>
        </router-link>
      </div>
      <div class="ui bottom attached active tab segment">
        <router-view :streetViewLink="streetViewLink" />
      </div>
    </div>
  </div>
</template>

<script>
import PropertyHeadline from "@/components/page/PropertyHeadline";
import { getPropertyLatestOwnerDetailsInfo } from "@/api/pages";

export default {
  name: "PropertyPage",
  components: {
    PropertyHeadline,
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
      ownerBasedResults: {
        violations: { rows: [] },
        complaints: { rows: [] },
      },
      latestRentalLicense: null,
      fullOwnersList: [],
      ownerTimelineData: [],
    };
  },
  methods: {
    isActive(name) {
      return this.$route.name === name;
    },
  },
  computed: {
    summaryLink() {
      return {
        name: "property-summary",
        params: { parcelNumber: this.parcelNumber },
      };
    },
    propertyDetailsLink() {
      return {
        name: "property-details",
        params: { parcelNumber: this.parcelNumber },
      };
    },
    ownerDetailsLink() {
      return {
        name: "owner",
        params: { parcelNumber: this.parcelNumber },
      };
    },
    loadingContent() {
      return (
        "Finding all " +
        this.loadingStep +
        " related information (may take some time)..."
      );
    },
  },
  created() {
    this.loading = true;
    // get all time-based data for the last year
    getPropertyLatestOwnerDetailsInfo(this.parcelNumber).then((result) => {
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
  },
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
