<script setup lang="ts">

import {onMounted} from "vue";
import {getPropertyDetailsPageInfo} from "../../services/apiFetcher.ts";
import ApexCharts from "apexcharts";

const props = defineProps({
  id: String
})
onMounted(async () => {
  const propertyResults = await getPropertyDetailsPageInfo(props.id)

  const timelineData = propertyResults["property_ownership_timeline"].map((data) => {
    return { x: data.owner, y: [ new Date(data.start.substring(0,10)).getTime(), new Date(data.end.substring(0,10)).getTime() ]}
  })
  const propertyValuePurchaseData = propertyResults["property_value_timeline"]
      .filter(data => data.status === "purchased").map((data) => {
        return { x: new Date(data.date.substring(0,10)).toLocaleString(), y: data.property_value}
      })

  const propertyValueAssesedData = propertyResults["property_value_timeline"]
      .filter(data => data.status === "assessed").map((data) => {
        return { x: new Date(data.date.substring(0,10)).toLocaleString(), y: data.property_value}
      })

  const timelineChart = new ApexCharts(document.querySelector('#timeline'), {
    series: [
      {
        data: timelineData
      }
    ],
    chart: {
      height: 250,
      type: 'rangeBar'
    },
    plotOptions: {
      bar: {
        horizontal: true
      }
    },
    xaxis: {
      type: 'datetime'
    }

  })

  const propertyValueChart= new ApexCharts(document.querySelector('#propertyValue'), {
    series: [
      {
        data: propertyValuePurchaseData
      },
      {
        data: propertyValueAssesedData
      },
    ],
    chart: {
      height: 250,
      type: 'area'
    },
    xaxis: {
      type: 'datetime'
    }

  })


  timelineChart.render().then()
  propertyValueChart.render().then()
})
</script>

<template>
  <div class="flex flex-col w-full">
    <h2>Who owned this property since 2000</h2>
    <section class="w-full">
      <div>
        <div id="timeline"></div>
      </div>
      <div>
        <div id="propertyValue"></div>
      </div>
    </section>
  </div>
</template>