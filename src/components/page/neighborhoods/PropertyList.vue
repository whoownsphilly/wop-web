<template>
  <div style="font-size: 18px">
    <h2>{{ name }}</h2>
    <a target="_blank" :href="directionsUrl">
      <a target="_blank" :href="pageUrl"
        >Link To read-only version of this List</a
      ><br /><br />
      Link to Walking Directions
    </a>
    <data-table :rows="propertyList" :title="name" />
    <span v-if="propertyList.length > 0">
      <leaflet-map-neighborhood
        :latLngs="propertyList"
        mapStyle="height: 350px; width: 100%"
        colorOverride="blue"
      />
    </span>
  </div>
</template>
<script>
import LeafletMapNeighborhood from "@/components/ui/LeafletMapNeighborhood";
import DataTable from "@/components/ui/DataTable";

export default {
  name: "NeighborhoodPropertyList",
  data() {
    return {};
  },
  components: {
    LeafletMapNeighborhood,
    DataTable
  },
  props: {
    name: {
      type: String,
      required: true
    },
    propertyList: {
      type: Array,
      required: true
    }
  },
  computed: {
    directionsUrl() {
      let locations = this.propertyList.map(
        x => `${x.location}, Philadelphia, PA`
      );
      return `https://www.google.com/maps/dir/${locations
        .join("/")
        .replaceAll(" ", "+")}/data=!4m2!4m1!3e2`;
    },
    pageUrl() {
      let parcelNumbers = this.propertyList.map(x => x.parcel_number);
      let query = {};
      query[this.name] = parcelNumbers;
      let url = this.$router.resolve({
        name: "NeighborhoodView",
        query: query
      });
      return `${window.location.origin}${url.href}`;
    }
  }
};
</script>
