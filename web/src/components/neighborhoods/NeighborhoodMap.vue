
<script setup lang="ts">
import L, {map, latLng, tileLayer, MapOptions, marker} from "leaflet";
import "leaflet.markercluster";
import {onMounted, watch} from "vue";
import 'leaflet/dist/leaflet.css';
import LeafletMap from "../ui/LeafletMap.vue";
const props = defineProps({
  properties: { type: Array, required: true}
});

let neighborhoodMap;

// const propertyFeatures = props.properties.map(p => {
//   return { "type": "Feature",
//     properties: {
//       address: p.opa_address,
//       color: p.color
//     },
//     geometry: {
//       type: "Point",
//       coordinates: [p.lng, p.lat]
//     },
//   }
// })


const propertyMarkers = props.properties.map(p => {
  return {
    latLng: latLng(p.lat, p.lng),
    color: p.color,
    popUp: p.location + " " + (p.unit || ""),
    parcelNumber: p.opa_account_num
  }
})
onMounted(() => {
  const options: MapOptions = {
    center: latLng(39.952583, -75.165222),
    zoom: 12,
  }

  neighborhoodMap  = map('neighborhoodMap', options)

  // 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
  tileLayer("https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
  }).addTo(neighborhoodMap);

  // const markers = L.markerClusterGroup();
  // props.properties.forEach(p => {
  //   const m = marker(latLng(p.lat, p.lng))
  //   markers.addLayer(m);
  // })
  // markers.addLayer(marker([39.952583, -75.165222]));
  // neighborhoodMap.addLayer(markers);
})

watch(() => props.properties,
    (value) => {
      // const markers = L.markerClusterGroup();
      // value.forEach(p => {
      //   const m = marker(latLng(p.lat, p.lng), { color: p.color})
      //   markers.addLayer(m);
      // })
      // propertyMap.addLayer(markers);
    })

</script>

<template>
  <LeafletMap id="neighborhoodMap" />
</template>

<style scoped></style>