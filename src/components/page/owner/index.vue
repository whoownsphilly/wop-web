<template>
<div>
    <h2>connected to {{ ownerTimelineData.length }} properties</h2>
    <sui-accordion exclusive>
      <div v-if="loadTables">
        <div v-for="table in tables" :key="table.name">
          <historical-tab-table
            searchType="owner"
            :searchToMatch="owner"
            :table="table"
          />
        </div>
      </div>
    </sui-accordion>
    <div v-if="timelineDataForChart">
     <vue-apex-charts type="rangeBar" :height="chartHeight" :options="chartOptions" :series="timelineDataForChart"></vue-apex-charts>
    </div>
  </div>
</template>

<script>
import HistoricalTabTable from "@/components/ui/HistoricalTabTable";
import VueApexCharts from 'vue-apexcharts'

export default {
  name: "HistoricalOwnerTab",
  components: { HistoricalTabTable, VueApexCharts},
  props: {
    owner: {
      type: String,
      required: true
    },
    ownerTimelineData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      latLngs: [],
      highlightedLatLng: null,
      loadTables: true,
      ownersList: [],
      isActive: {},
      tables: [
        { title: "Violations", name: "violations" },
        { title: "Complaints", name: "complaints" },
        { title: "Appeals", name: "appeals" },
        { title: "Case Investigations", name: "case_investigations" }
      ],

          chartOptions: {
            chart: {
              type: 'rangeBar'
            },
            plotOptions: {
              bar: {
                horizontal: true
              }
            },
            tooltip: {
                x: {format: 'dd MMM, yyyy'}
            },
            yaxis: {
              labels: {maxWidth: 250}
            },
            xaxis: {
              type: 'datetime'
            }
          }
    };
  },
  computed: {
    chartHeight(){return this.ownerTimelineData.length * 10},
    timelineDataForChart() {
      let dataForChart = []
      this.ownerTimelineData.forEach(time => {
          dataForChart.push({x: time.name, y: [time.start.getTime(), time.end.getTime()]})
      })
      return  [{data:  dataForChart }]
    }
  },
};
</script>
