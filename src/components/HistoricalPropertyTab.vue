<template>
  <div>
    <sui-accordion exclusive>
          <sui-accordion-title>
            <h2><sui-icon name="dropdown" /> Timeline</h2>
          </sui-accordion-title>
          <sui-accordion-content>
            <div v-if="timelineData">
                <vue-timeline :data="timelineData"></vue-timeline>
            </div>
          </sui-accordion-content>
        <div v-for="table in tables" :key="table.name">
          <sui-accordion-title>
            <h2><sui-icon name="dropdown" /> {{table.title }}</h2>
          </sui-accordion-title>
          <sui-accordion-content>
            <historical-tab-table searchType="parcel_number" :searchToMatch="parcelNumber" :tableName="table.name"/>
          </sui-accordion-content>
          </div>
    </sui-accordion>
  </div>
</template>

<script>
import HistoricalTabTable from '@/components/HistoricalTabTable'
import { getTableInfo } from '@/api/singleTable'
import VueTimeline from "vue-timeline-component"

export default {
  name: "HistoricalPropertyTab",
  components: {HistoricalTabTable, VueTimeline},
  props: {
      parcelNumber: {
          type: String,
          required: true
      }
  },
  data() {
    return {
        timelineData: null,
        tables: [
            {"title": "Violations", "name": "violations"},
            {"title": "Complaints", "name": "complaints"},
            {"title": "Appeals", "name": "appeals"},
            {"title": "Case Investigations", "name": "case_investigations"},
        ],
    }
  },
  created() {
    getTableInfo('real_estate_transfers', 'parcel_number', this.parcelNumber)
    .then(data => {
        if ("results" in data) {
          const timelineData = []
          let prevEndDate = null
          let lastGrantees = null
          for(let i in data.results.rows){
              let row = data.results.rows[i]
              row.name = row.grantors
              row.start = new Date(Date.parse(prevEndDate || row.year_built))
              row.end = new Date(Date.parse(row.receipt_date))
              prevEndDate = row.end
              lastGrantees = row.grantees
              let output = {
                  name: row.name,
                  start: row.start,
                  end: row.end,
              }
              timelineData.push(output)
            }
          timelineData.push({
              name: lastGrantees,
              start: prevEndDate,
              end: new Date()
          })
          this.timelineData = timelineData
        }
      });
  }
};
</script>
