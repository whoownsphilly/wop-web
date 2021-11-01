<template>
    <div v-if="dataForChart">
        <vue-apex-charts type="area" height="350" :options="chartOptions" :series="dataForChart"/>
    </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: "VueApexLineChart",
  components: { VueApexCharts},
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
          chartOptions: {
            chart: {
              type: 'area',
              height: 350,
              zoom: {
                enabled: false
              }
            },
            dataLabels: {
              enabled: false
            },
            stroke: {
              curve: 'straight'
            },
            xaxis: {
              type: 'datetime',
            },
            yaxis: {
              title: { text: '$ (Dollars)' }
            },
            tooltip: {
              x: {
                format: "yyyy-MM-dd",
              }
            },
            legend: {
              horizontalAlign: 'left'
            }
          },
    };
  },
  computed: {
    chartHeight(){return this.data.length * 50},
    dataForChart() {
      // This is currently overly hardcoded for 2 lines with the 
      // assessment value chart but can be generalized
      // if this gets used elseshwere.
      let allSeriesData = []
      let data1ForChart = []
      let data2ForChart = []
      let dtCol = "date"
      this.data.forEach(dataPoint => {
          let dt = new Date(Date.parse(dataPoint[dtCol])).getTime() 
          if(dataPoint.status === "purchased"){
              data1ForChart.push({
                  x: dt, y: dataPoint.property_value 
              })
            }
      })
      allSeriesData.push({name: "Value at Purchase (Whole Deed)", data: data1ForChart})
      this.data.forEach(dataPoint => {
          let dt = new Date(Date.parse(dataPoint[dtCol])).getTime() 
          if(dataPoint.status === "assessed"){
              data2ForChart.push({
                  x: dt, y: dataPoint.property_value 
              })
          }
      })
      allSeriesData.push({name: "Value for Assessment (Single Unit)", data: data2ForChart})
      return allSeriesData
    }
  },
};
</script>
