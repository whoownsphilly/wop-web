<template>
  <div style="font-size: 18px">
    <leaflet-map :latLngs="properties" :highlightedLatLngs="thisProperty" />
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
    }
  },
  data() {
    return {
      nProperties: null,
      thisProperty: null
    };
  }
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
