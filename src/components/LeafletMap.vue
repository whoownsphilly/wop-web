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
      <l-geo-json
        :geojson="geojson"
        :options="options"
        :options-style="styleFunction"
      />
      <div v-for="(marker, index) in mapMarkers" :key="index">
        <l-marker :lat-lng="marker" />
      </div>
    </l-map>
  </div>
</template>

<script>
import { latLngBounds, latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LGeoJson } from "vue2-leaflet";

export default {
  name: "Example",
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LMarker
  },
  props: {
    latLngs: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      zoom: 6,
      center: [48, -1.219482],
      geojson: null,
      fillColor: "#e4ce7f",
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    };
  },
  computed: {
    mapMarkers() {
      return this.latLngs.map(latLngTuple =>
        latLng(latLngTuple.lat, latLngTuple.lng)
      );
    },
    mapBounds() {
      return latLngBounds(
        this.latLngs.map(latLngTuple => [latLngTuple.lat, latLngTuple.lng])
      );
    },
    options() {
      return {
        onEachFeature: this.onEachFeatureFunction
      };
    },
    styleFunction() {
      return () => {
        return {
          weight: 2,
          color: "#ECEFF1",
          opacity: 1,
          fillColor: this.fillColor,
          fillOpacity: 1
        };
      };
    },
    onEachFeatureFunction() {
      return (feature, layer) => {
        layer.bindTooltip(
          "<div>code:" +
            feature.properties.code +
            "</div><div>nom: " +
            feature.properties.nom +
            "</div>",
          { permanent: false, sticky: true }
        );
      };
    }
  },
  async created() {
    this.loading = true;
    const response = await fetch(
      "https://rawgit.com/gregoiredavid/france-geojson/master/regions/pays-de-la-loire/communes-pays-de-la-loire.geojson"
    );
    const data = await response.json();
    this.geojson = data;
    this.loading = false;
  }
};
</script>
