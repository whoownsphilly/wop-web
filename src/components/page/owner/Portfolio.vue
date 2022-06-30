<template>
  <div style="font-size: 18px">
    Click on a property to see the address. If you click on the address that
    pops up, it will take you to that property's page.
    <leaflet-map :latLngs="properties" :highlightedLatLng="thisProperty" />
  </div>
</template>
<script>
import LeafletMap from "@/components/ui/LeafletMap";

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
    thisProperty: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      nProperties: null
    };
  }
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
