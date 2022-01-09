<template>
  <div style="font-size: 18px">
    The owner of this property is currently associated with
    <b>{{ properties.length }}</b> properties valued at
    <b>{{ totalValueOfProperties }}</b
    ><sup><info-modal modalName="owner.portfolio.marketValueInfo"/></sup>.
    Across all of these properties, there have been an average of
    <b>{{ violationsPerProperty }}</b> violations per property,
    <b>{{ openViolationsPerProperty }}</b> of which are currently open. These
    properties have an average of
    <b>{{ violationsPerPropertyPerDay }}</b> violations per property per day.
    This is {{ violationRelativeToText }} the city-wide average of
    <b>{{ precomputedAvgViolationsPerPropertyPerDay }}</b> violations per
    property per day.

    <leaflet-map :latLngs="properties" :highlightedLatLngs="thisProperty" />
  </div>
</template>
<script>
import LeafletMap from "@/components/ui/LeafletMap";
import { formatCurrencyValue } from "@/components/utils/formatting.js";

export default {
  name: "PropertyPortfolio",
  components: {
    LeafletMap
  },
  props: {
    properties: {
      type: Array,
      required: true
    },
    mailingAddressBasedOwnerPortfolio: {
      type: Object,
      required: true
    },
    ownerBasedOwnerPortfolio: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      precomputedAvgViolationsPerPropertyPerDay: 0.007,
      nProperties: null,
      thisProperty: null,
      totalViolations:
        this.ownerBasedOwnerPortfolio.violations.all.total_violations +
        this.mailingAddressBasedOwnerPortfolio.violations.all.total_violations,
      totalViolationsOpen:
        this.ownerBasedOwnerPortfolio.violations.open.total_violations +
        this.mailingAddressBasedOwnerPortfolio.violations.open.total_violations,
      totalViolationDays:
        this.ownerBasedOwnerPortfolio.violations.all.total_violation_days +
        this.mailingAddressBasedOwnerPortfolio.violations.all
          .total_violation_days,
      totalViolationProperties:
        this.ownerBasedOwnerPortfolio.violations.all
          .total_violation_properties +
        this.mailingAddressBasedOwnerPortfolio.violations.all
          .total_violation_properties
    };
  },
  computed: {
    violationRelativeToText() {
      return this.violationsPerPropertyPerDay >
        this.precomputedAvgViolationsPerPropertyPerDay
        ? "above"
        : "below";
    },
    openViolationsPerProperty() {
      if (this.totalViolationProperties === 0) {
        return 0;
      }
      return (
        Math.round(
          (1000 * this.totalViolationsOpen) / this.totalViolationProperties
        ) / 1000
      );
    },
    violationsPerProperty() {
      if (this.totalViolationProperties === 0) {
        return 0;
      }
      return (
        Math.round(
          (1000 * this.totalViolations) / this.totalViolationProperties
        ) / 1000
      );
    },
    violationsPerPropertyPerDay() {
      if (this.totalViolationDays === 0) {
        return 0;
      }
      return (
        Math.round((10000 * this.totalViolations) / this.totalViolationDays) /
        10000
      );
    },
    totalValueOfProperties() {
      var totalValue = 0;
      for (var i = 0; i < this.properties.length; i++) {
        totalValue += this.properties[i].market_value;
      }
      return formatCurrencyValue(totalValue);
    }
  }
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
