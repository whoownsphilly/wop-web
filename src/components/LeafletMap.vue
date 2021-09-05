<template>
  <div>
    <div></div>
    <l-map
      :zoom="zoom"
      :center="center"
      :bounds="mapBounds"
      style="height: 500px; width: 100%"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <div v-for="(marker, index) in mapMarkers" :key="index">
        <l-circle-marker :lat-lng="marker.latLng" :color="marker.color" />
      </div>
      <div v-if="highlightedMapMarker">
        <l-circle-marker :lat-lng="highlightedMapMarker.latLng" 
        zIndeOffset=0
        :color="highlightedMapMarker.color" />
      </div>
    </l-map>
  </div>
</template>

<script>
import { latLngBounds, latLng } from "leaflet";
import { LMap, LTileLayer, LCircleMarker } from "vue2-leaflet";

export default {
  name: "Example",
  components: {
    LMap,
    LTileLayer,
    LCircleMarker
  },
  props: {
    latLngs: {
      type: Array,
      required: true
    },
    highlightedLatLng: {
      type: Object
    }
  },
  data() {
    return {
      loading: false,
      highlightedCircleWeight: 100,
      zoom: 6,
      center: [48, -1.219482],
      fillColor: "#e4ce7f",
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    };
  },
  computed: {
    highlightedMapMarker() {
      if (this.highlightedLatLng) {
        return {"latLng": latLng(this.highlightedLatLng.lat, this.highlightedLatLng.lng), "color": "black"};
      } else {
        return null;
      }
    },
    mapMarkers() {
      return this.latLngs.map(latLngTuple =>
        ({"latLng": latLng(latLngTuple.lat, latLngTuple.lng), "color": latLngTuple.color})
      );
    },
    mapBounds() {
      return latLngBounds(
        this.latLngs.map(latLngTuple => [latLngTuple.lat, latLngTuple.lng])
      );
    }
  },
  async created() {}
};
</script>
