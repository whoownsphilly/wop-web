<script setup lang="ts">
import L, { map, latLng, tileLayer, MapOptions, marker, circleMarker } from 'leaflet'
import 'leaflet.markercluster'
import { onMounted, watch } from 'vue'
import LeafletMap from '../ui/LeafletMap.vue'

const props = defineProps({
  properties: { type: Array, required: true },
})

let propertyMap: any

const getColors = (property: any) => {
  switch (property.color) {
    case 'red':
      return ['#ef4444', '#991b1b']
    case 'blue':
      return ['#6366f1', '#3730a3']
    default:
      return ['#737373', '#262626']
  }
}

const createCircleMarker = (property: any) => {
  const colors = getColors(property)
  const marker = circleMarker(latLng(property.lat, property.lng), {
    color: colors[0],
    fill: true,
    fillColor: colors[1],
    fillOpacity: 0.6,
  })
  const url = `/properties/${property.opa_account_num}/owner`
  marker.bindPopup(
    `<a class="underline" href="${url}">${property.location} ${property.unit || ''}</a>`
  )

  return marker
}

const setMarkers = (properties: any[]) => {
  const markers = L.markerClusterGroup()
  properties.forEach((p: any) => {
    const m = createCircleMarker(p)
    markers.addLayer(m)
  })
  propertyMap.addLayer(markers)
}
onMounted(() => {
  const options: MapOptions = {
    center: latLng(39.952583, -75.165222),
    zoom: 14,
  }

  propertyMap = map('propertyMap', options)

  const tileDomain = import.meta.env.PUBLIC_MAP_TILE_DOMAIN || 'https://tile.openstreetmap.org'
  tileLayer(`${tileDomain}/{z}/{x}/{y}.png`, {
    maxZoom: 19,
    attribution: '',
  }).addTo(propertyMap)

  //
  const legend = L.control({ position: 'bottomleft' })
  legend.onAdd = function () {
    const div = L.DomUtil.create('div', 'bg-white p-2 border border-black flex flex-col opacity-95')
    div.innerHTML =
      '' +
      "<div><span class='bg-black px-2 py-1 mr-2'></span>This Property</div>" +
      "<div><span class='bg-red-500 px-2 py-1 mr-2'></span><span>Same Mailing Address</span></div>" +
      "<div><span class='bg-indigo-500 px-2 py-1 mr-2'></span><span>Same Owner</span></div>"

    return div
  }
  legend.addTo(propertyMap)

  propertyMap.addControl(legend)

  setMarkers(props.properties)
})

watch(
  () => props.properties,
  (value: any) => {
    setMarkers(value)
  }
)
</script>

<template>
  <LeafletMap id="propertyMap" />
</template>

<style scoped></style>
