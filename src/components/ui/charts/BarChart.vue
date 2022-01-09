<template>
  <div v-if="dataForChart">
    <vue-apex-charts
      type="bar"
      height="350"
      :options="chartOptions"
      :series="dataForChart"
    />
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "VueApexBarChart",
  components: { VueApexCharts },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dataForChart: this.data.data,
      chartOptions: {
        chart: { type: "bar", height: 350, stacked: true },
        plotOptions: { bar: { horizontal: true } },
        stroke: { width: 1, colors: ["#000"] },
        title: { text: "Number of Properties Owned by Owner Name" },
        xaxis: {
          categories: this.data.categories,
          labels: {
            formatter: function(val) {
              return val;
            }
          }
        },
        yaxis: { title: { text: "Owner Name" }, labels: { maxWidth: 600 } },
        tooltip: {
          y: {
            formatter: function(val) {
              return val + " properties";
            }
          }
        },
        fill: { opacity: 1 },
        legend: { position: "top", horizontalAlign: "left", offsetX: 40 }
      }
    };
  }
};
</script>
