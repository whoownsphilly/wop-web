<template>
  <div>
    Click on a property to see the address. If you click on the address that
    pops up, it will take you to that property's page.
    <l-map
      :zoom="zoom"
      :center="center"
      :bounds="mapBounds"
      :sleep="true"
      :options="leafletOptions"
      style="height: 500px; width: 100%"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <div v-for="(marker, index) in mapMarkers" :key="index">
        <l-circle-marker
          :lat-lng="marker.latLng"
          :color="marker.color"
          :fillColor="marker.color"
        >
          <l-popup>
            <div @click="jumpToProperty(marker.parcelNumber)">
              <a class="hyperlink"
                ><u>{{ marker.popUp }}</u></a
              >
            </div>
          </l-popup>
        </l-circle-marker>
      </div>
      <div v-if="highlightedMapMarker">
        <v-marker-cluster>
          <l-circle-marker
            :lat-lng="highlightedMapMarker.latLng"
            zIndexOffset="0"
            :color="highlightedMapMarker.color"
            :fillColor="highlightedMapMarker.color"
          >
            <l-popup>
              {{ highlightedMapMarker.popUp }}
            </l-popup>
          </l-circle-marker>
        </v-marker-cluster>
      </div>
      <l-control class="legend" :position="'bottomleft'">
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
      leafletOptions: { scrollWheelZoom: false },
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
    jumpToProperty(parcelNumber) {
      this.$router.push("/property/" + parcelNumber);
      this.$router.go();
    }
  },
  async created() {}
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
