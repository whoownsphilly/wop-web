<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getPropertyDetailsPageInfo } from '../../services/apiFetcher.ts'
import ApexCharts from 'apexcharts'

const props = defineProps({
  id: String,
})

const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  try {
    const propertyResults = await getPropertyDetailsPageInfo(props.id)

    const timelineData = propertyResults['property_ownership_timeline'].map((data) => {
      return {
        x: data.owner,
        y: [
          new Date(data.start.substring(0, 10)).getTime(),
          new Date(data.end.substring(0, 10)).getTime(),
        ],
      }
    })
    const propertyValuePurchaseData = propertyResults['property_value_timeline']
      .filter((data) => data.status === 'purchased')
      .map((data) => {
        return { x: new Date(data.date.substring(0, 10)).toLocaleString(), y: data.property_value }
      })

    const propertyValueAssesedData = propertyResults['property_value_timeline']
      .filter((data) => data.status === 'assessed')
      .map((data) => {
        return { x: new Date(data.date.substring(0, 10)).toLocaleString(), y: data.property_value }
      })

    const timelineChart = new ApexCharts(document.querySelector('#timeline'), {
      series: [
        {
          data: timelineData,
        },
      ],
      chart: {
        height: 250,
        type: 'rangeBar',
      },
      plotOptions: {
        bar: {
          horizontal: true,
        },
      },
      xaxis: {
        type: 'datetime',
      },
    })

    const propertyValueChart = new ApexCharts(document.querySelector('#propertyValue'), {
      series: [
        {
          data: propertyValuePurchaseData,
        },
        {
          data: propertyValueAssesedData,
        },
      ],
      chart: {
        height: 250,
        type: 'area',
      },
      xaxis: {
        type: 'datetime',
      },
    })

    await Promise.all([timelineChart.render(), propertyValueChart.render()])
  } catch (error) {
    console.error('Error loading timeline data:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div>
    <div v-if="isLoading" class="mb-4 flex justify-between rounded-sm bg-gray-200 p-4">
      <div class="w-full text-center">
        <span>Loading timeline data...</span>
      </div>
      <div
        class="h-5 w-5 animate-spin rounded-full border-2 border-emerald-800 border-t-transparent"
      ></div>
    </div>
    <template v-else>
      <div id="timeline"></div>
      <div id="propertyValue"></div>
    </template>
  </div>
</template>

<style scoped></style>
