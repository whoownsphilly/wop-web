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
          {{ marker.popUp }}<br />
          <span
            v-if="customPropertyLists && customPropertyListNames.length > 0"
          >
            Choose a List Name from the dropdown:
            <sui-dropdown
              :options="customPropertyListNames"
              placeholder="Property List"
              fluid
              selection
              v-model="selectedPropertyListName"
            />
            <span v-if="selectedPropertyListName">
              <sui-button size="mini" v-on:click="addProperty(marker)"
                >Add to {{ selectedPropertyListName }}</sui-button
              >
            </span>
          </span>
          <span v-else-if="customPropertyLists"
            >No lists found, you need to add a List using the "+ (Add List)" tab
            below</span
          >
        </l-popup>
      </l-circle-marker>
    </l-map>
  </div>
</template>

<script>
import { latLngBounds, latLng } from "leaflet";
import LDrawToolbar from "vue2-leaflet-draw-toolbar";

import { LMap, LTileLayer, LCircleMarker, LPopup } from "vue2-leaflet";

export default {
  name: "LeafletMapNeighborhood",
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LCircleMarker,
    LDrawToolbar,
  },
  props: {
    latLngs: {
      type: Array,
      required: true,
    },
    mapStyle: {
      type: String,
      default: "height: 500px; width: 100%",
    },
    customPropertyLists: {
      type: Object,
    },
    colorOverride: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      selectedPropertyListName: null,
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
        color: this.colorOverride || latLngTuple.color,
        popUp: latLngTuple.location + " " + (latLngTuple.unit || ""),
        parcelNumber: latLngTuple.parcel_number,
      }));
    },
    mapBounds() {
      if (this.latLngs.length > 0) {
        return latLngBounds(
          this.latLngs.map((latLngTuple) => [latLngTuple.lat, latLngTuple.lng])
        );
      } else {
        return latLngBounds([
          [39.977523, -75.136808],
          [39.922655, -75.193699],
        ]);
      }
    },
  },
  methods: {
    updateBounds(bounds) {
      this.$emit("updateBounds", bounds);
    },
    drawnBounds(e) {
      this.$emit("updateBounds", e.layer._bounds);
      let selectedMarkers = [];
      this.mapMarkers.map((marker) => {
        if (this.isMarkerInsidePolygon(marker, e.layer)) {
          selectedMarkers.push(marker);
        }
      });
      this.$emit("selectMarkers", selectedMarkers);
    },
    addProperty(marker) {
      this.$refs.map.mapObject.closePopup();
      this.$emit("addProperty", this.selectedPropertyListName, marker);
      this.selectedPropertyListName = "";
    },

    isMarkerInsidePolygon(marker, poly) {
      var polyPoints = poly.getLatLngs()[0];
      var x = marker.latLng.lat,
        y = marker.latLng.lng;

      var inside = false;
      for (
        var i = 0, j = polyPoints.length - 1;
        i < polyPoints.length;
        j = i++
      ) {
        var xi = polyPoints[i].lat;
        var yi = polyPoints[i].lng;
        var xj = polyPoints[j].lat;
        var yj = polyPoints[j].lng;

        var intersect =
          yi > y != yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
        if (intersect) inside = !inside;
      }

      return inside;
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
