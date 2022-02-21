<template>
  <div style="font-size: 18px">
    <leaflet-map
      :latLngs="properties"
      @updateBounds="updatePropertyList"
      mapStyle="height: 350px; width: 100%"
      includeLegend="includeLegend"
    />
    <data-table :rows="properties" title="Properties" />
  </div>
</template>
<script>
import LeafletMap from "@/components/ui/LeafletMap";
import DataTable from "@/components/ui/DataTable";
import { getNeighborhoodsPageInfo } from "@/api/pages";

export default {
  name: "NeighborhoodView",
  components: {
    LeafletMap,
    DataTable,
  },
  methods: {
    updatePropertyList(bounds) {
      getNeighborhoodsPageInfo(bounds).then(
        (results) => (this.properties = results.properties)
      );
    },
  },
  data() {
    return {
      includeLegend: false,
      rows: [],
      columns: [],
      properties: [
        {
          lat: 39.94960043271942,
          lng: -75.1645923794803,
          location: "ABC Spot",
          unit: "",
        },
      ],
    };
  },
  created() {},
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
