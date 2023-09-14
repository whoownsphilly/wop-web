
<script setup lang="ts">
import L, {map, latLng, tileLayer, MapOptions, marker} from "leaflet";
import "leaflet.markercluster";
import {onMounted, watch} from "vue";
import LeafletMap from "../ui/LeafletMap.vue";

const props = defineProps({
  properties: { type: Array, required: true}
});

let propertyMap;

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

  propertyMap  = map('propertyMap', options)

  // 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
  tileLayer("https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
  }).addTo(propertyMap);

  const markers = L.markerClusterGroup();
    props.properties.forEach(p => {
       const m = marker(latLng(p.lat, p.lng))
       markers.addLayer(m);
    })
  markers.addLayer(marker([39.952583, -75.165222]));
// add more markers here...

  propertyMap.addLayer(markers);


})

watch(() => props.properties,
    (value) => {
  console.log("watch")
      console.log(propertyMap)
      const markers = L.markerClusterGroup();
      value.forEach(p => {
        const m = marker(latLng(p.lat, p.lng), { color: p.color})
        markers.addLayer(m);
      })
      propertyMap.addLayer(markers);
})
  // return this.latLngs.map(latLngTuple => ({
  //   latLng: latLng(latLngTuple.lat, latLngTuple.lng),
  //   color: latLngTuple.color,
  //   popUp: latLngTuple.location + " " + (latLngTuple.unit || ""),
  //   parcelNumber: latLngTuple.opa_account_num
  // }));

// mymap .on("load", () => {
//     if(propertyFeatures.length > 0) {
//       map.addSource("properties", {
//         type: "geojson",
//         data:  {
//           "type": "FeatureCollection",
//           "crs": { "type": "name", "properties": {} },
//           "features": propertyFeatures
//         },
//         cluster: true,
//         clusterMaxZoom: 14, // Max zoom to cluster points on
//         clusterRadius: 50 // Radius of each cluster when clustering points (defaults to 50)
//       });
//       map.addLayer({
//         id: "clusters",
//         type: "circle",
//         source: "properties",
//         filter: ["has", "point_count"],
//         paint: {
//           // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
//           // with three steps to implement three types of circles:
//           //   * Blue, 20px circles when point count is less than 100
//           //   * Yellow, 30px circles when point count is between 100 and 750
//           //   * Pink, 40px circles when point count is greater than or equal to 750
//           "circle-color": [
//             "step",
//             ["get", "point_count"],
//             "#10b981",
//             5,
//             "#34d399",
//             25,
//             "#6ee7b7"
//           ],
//           "circle-radius": [
//             "step",
//             ["get", "point_count"],
//             20,
//             100,
//             30,
//             750,
//             40
//           ]
//         }
//       });
//       map.addLayer({
//         id: "cluster-count",
//         type: "symbol",
//         source: "properties",
//         filter: ["has", "point_count"],
//         layout: {
//           "text-field": ["get", "point_count_abbreviated"],
//           "text-font": ["DIN Offc Pro Medium", "Arial Unicode MS Bold"],
//           "text-size": 12
//         }
//       });
//       map.addLayer({
//         id: "unclustered-point",
//         type: "circle",
//         source: "properties",
//         filter: ["!", ["has", "point_count"]],
//         paint: {
//           "circle-color": "#059669",
//           "circle-radius": 4,
//           "circle-stroke-width": 1,
//           "circle-stroke-color": "#cccccc"
//         }
//       });
//
//       // inspect a cluster on click
//       map.on("click", "clusters", (e) => {
//         const features = map.queryRenderedFeatures(e.point, {
//           layers: ["clusters"]
//         });
//         const clusterId = features[0].properties.cluster_id;
//         map.getSource("properties").getClusterExpansionZoom(
//             clusterId,
//             (err, zoom) => {
//               if (err) return;
//
//               map.easeTo({
//                 center: features[0].geometry.coordinates,
//                 zoom: zoom
//               });
//             }
//         );
//       });
//
//       map.on("mouseenter", "clusters", () => {
//         map.getCanvas().style.cursor = "pointer";
//       });
//       map.on("mouseleave", "clusters", () => {
//         map.getCanvas().style.cursor = "";
//       });
//     }
//
//   })
</script>

<template>
  <LeafletMap id="propertyMap" />
</template>

<style scoped></style>