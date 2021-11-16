<template>
    <div v-if="timelineDataForChart">
     <vue-apex-charts type="rangeBar" :height="chartHeight" :options="chartOptions" :series="timelineDataForChart"></vue-apex-charts>
    </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: "VueApexTimeline",
  components: { VueApexCharts},
  props: {
    labelCol: {
      type: String,
      required: true

    },
    startCol: {
      type: String,
      default: function() {return "start"}
    },
    endCol: {
      type: String,
      default: function() {return "end"}
    },
    data: {
      type: Array,
      required: true

    }
  },
  data() {
    return {

          chartOptions: {
            chart: {
              type: 'rangeBar'
            },
            plotOptions: {
              bar: {
                  barHeight: '80%',
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
    chartHeight(){return Math.max(this.data.length * 50, 200)},
    timelineDataForChart() {
      let dataForChart = []
      this.data.forEach(time => {
          let startTime = new Date(Date.parse(time[this.startCol])).getTime() 
          let endTime = new Date(Date.parse(time[this.endCol]) || Date()).getTime() 
          let label = time[this.labelCol]
          let labelList = []
          if(label.indexOf(';') >= 0){
            labelList = label.split(';')
          }
          else if(label.length > 25){
              let maxLength = 20
              let labelSplitIndex = label.substring(maxLength,label.length - 1).indexOf(' ') + maxLength
              labelList = [label.substring(0,labelSplitIndex), label.substring(labelSplitIndex)]
          }
          else { labelList = label}

          dataForChart.push({
              x: labelList, y: [startTime, endTime] 
          })
      })
      return  [{data:  dataForChart }]
    }
  },
};
</script>
