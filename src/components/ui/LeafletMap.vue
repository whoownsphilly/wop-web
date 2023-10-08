<script setup lang="ts">
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  id: String
})
</script>

<template>
  <div :id="id" class="w-full h-full"></div>
</template>