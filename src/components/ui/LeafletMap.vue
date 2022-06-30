<template>
  <div>
    <l-map
      :zoom="zoom"
      :center="center"
      :bounds="mapBounds"
      @update:bounds="updateBounds"
      :sleep="true"
      :options="leafletOptions"
      :style="mapStyle"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <vue2-leaflet-marker-cluster>
        <l-circle-marker
          :lat-lng="marker.latLng"
          v-for="(marker, index) in mapMarkers"
          :key="index"
          :color="marker.color"
          :fillColor="marker.color"
        >
          <l-popup>
            <a
              class="hyperlink"
              target="_blank"
              :href="propertyUrl(marker.parcelNumber)"
              ><u>{{ marker.popUp }}</u></a
            >
          </l-popup>
        </l-circle-marker>
      </vue2-leaflet-marker-cluster>
      <div v-if="highlightedMapMarker">
        <l-circle-marker
          :lat-lng="highlightedMapMarker.latLng"
          zIndexOffset="0"
          color="black"
          fillColor="black"
        >
          <l-popup>
            {{ highlightedMapMarker.popUp }}
          </l-popup>
        </l-circle-marker>
      </div>
      <l-control v-if="includeLegend" class="legend" :position="'bottomleft'">
        <i style="background: black"></i><span>This Property</span><br />
        <i style="background: blue"></i><span>Same Mailing Address</span><br />
        <i style="background: red"></i><span>Same Owner</span><br />
      </l-control>
    </l-map>
  </div>
</template>

<script>
import { latLngBounds, latLng } from "leaflet";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster";
import {
  LMap,
  LTileLayer,
  LCircleMarker,
  LControl,
  LPopup
} from "vue2-leaflet";

export default {
  name: "LeafletMap",
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LControl,
    LCircleMarker,
    Vue2LeafletMarkerCluster
  },
  props: {
    latLngs: {
      type: Array,
      required: true
    },
    includeLegend: {
      type: Boolean,
      default: true
    },
    mapStyle: {
      type: String,
      default: "height: 500px; width: 100%"
    },
    highlightedLatLng: {
      type: Object
    }
  },
  data() {
    return {
      loading: false,
      leafletOptions: { scrollWheelZoom: false },
      highlightedCircleWeight: 100,
      zoom: 6,
      center: [48, -1.219482],
      fillColor: "#e4ce7f",
      //url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      url: "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    };
  },
  computed: {
    highlightedMapMarker() {
      if (this.highlightedLatLng) {
        return {
          latLng: latLng(
            this.highlightedLatLng.lat,
            this.highlightedLatLng.lng
          ),
          color: "black",
          parcelNumber: this.highlightedLatLng.parcel_number,
          popUp:
            this.highlightedLatLng.location +
            " " +
            (this.highlightedLatLng.unit || "")
        };
      } else {
        return null;
      }
    },
    mapMarkers() {
      return this.latLngs.map(latLngTuple => ({
        latLng: latLng(latLngTuple.lat, latLngTuple.lng),
        color: latLngTuple.color,
        popUp: latLngTuple.location + " " + (latLngTuple.unit || ""),
        parcelNumber: latLngTuple.opa_account_num
      }));
    },
    mapBounds() {
      return latLngBounds(
        this.latLngs.map(latLngTuple => [latLngTuple.lat, latLngTuple.lng])
      );
    }
  },
  methods: {
    updateBounds(bounds) {
      this.$emit("updateBounds", bounds);
    },
    propertyUrl(parcelNumber) {
      return `#/property/${parcelNumber}`;
    },
    jumpToProperty(parcelNumber) {
      this.$router.push("/property/" + parcelNumber);
      this.$router.go();
    }
  },
  async created() {}
};
</script>
<style>
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
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
