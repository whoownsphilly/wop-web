<template>
  <div>
    <l-map
      :zoom="zoom"
      ref="map"
      :center="center"
      :bounds="mapBounds"
      @update:bounds="updateBounds"
      @draw:created="drawnBounds"
      :sleep="true"
      :options="leafletOptions"
      :style="mapStyle"
    >
      <l-draw-toolbar />
      <l-tile-layer :url="url" :attribution="attribution" />
      <l-circle-marker
        :lat-lng="marker.latLng"
        v-for="(marker, index) in mapMarkers"
        :key="index"
        :color="marker.color"
        :fillColor="marker.color"
      >
        <l-popup>
          <sui-dropdown
            :options="customPropertyListNames"
            placeholder="Property List"
            fluid
            search
            selection
            v-model="selectedPropertyListName"
          />
          <a v-on:click="addProperty(marker)">{{ marker.popUp }}</a>
        </l-popup>
      </l-circle-marker>
      <l-control v-if="includeLegend" class="legend" :position="'bottomleft'">
        <i style="background: black"></i><span>This Property</span><br />
        <i style="background: yellow"></i><span>Same Mailing Address</span
        ><br />
        <i style="background: red"></i><span>Same Owner</span><br />
      </l-control>
    </l-map>
  </div>
</template>

<script>
import { latLngBounds, latLng } from "leaflet";
import LDrawToolbar from "vue2-leaflet-draw-toolbar";

import {
  LMap,
  LTileLayer,
  LCircleMarker,
  LControl,
  LPopup,
} from "vue2-leaflet";

export default {
  name: "LeafletMapNeighborhood",
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LControl,
    LCircleMarker,
    LDrawToolbar,
  },
  props: {
    latLngs: {
      type: Array,
      required: true,
    },
    includeLegend: {
      type: Boolean,
      default: true,
    },
    mapStyle: {
      type: String,
      default: "height: 500px; width: 100%",
    },
    customPropertyLists: {
      type: Object,
    },
  },
  data() {
    return {
      loading: false,
      selectedPropertyListName: "abc",
      leafletMap: null,
      leafletOptions: { scrollWheelZoom: false },
      zoom: 6,
      center: [48, -1.219482],
      fillColor: "#e4ce7f",
      //url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      url: "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    };
  },
  computed: {
    layers() {
      let layers = [];
      this.$refs.map.mapObject.eachLayer(function(layer) {
        layers.push(layer);
      });
      return layers;
    },
    customPropertyListNames() {
      return Object.keys(this.customPropertyLists).map((x) => ({
        text: x,
        value: x,
      }));
    },
    mapMarkers() {
      return this.latLngs.map((latLngTuple) => ({
        latLng: latLng(latLngTuple.lat, latLngTuple.lng),
        color: latLngTuple.color,
        popUp: latLngTuple.location + " " + (latLngTuple.unit || ""),
        parcelNumber: latLngTuple.parcel_number,
      }));
    },
    mapBounds() {
      return latLngBounds(
        this.latLngs.map((latLngTuple) => [latLngTuple.lat, latLngTuple.lng])
      );
    },
  },
  methods: {
    updateBounds(bounds) {
      this.$emit("updateBounds", bounds);
    },
    drawnBounds(e) {
      this.$emit("updateBounds", e.layer._bounds);
    },
    addProperty(marker) {
      this.$refs.map.mapObject.closePopup();
      this.$emit("addProperty", this.selectedPropertyListName, marker);
      this.selectedPropertyListName = "";
    },
  },
};
</script>
<style>
.legend {
  background: white;
  opacity: 0.9;
}
.legend i {
  width: 18px;
  height: 18px;
  float: left;
  margin: 0 8px 0 0;
  opacity: 0.7;
}
.hyperlink {
  color: #0000ff;
  text-decoration: underline;
}
</style>
