<template>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader content="Finding All Information for this property..." />
    </sui-dimmer>
  </div>
  <div v-else>
    <div v-if="timelineData">
      <div id="timeline" />
    </div>
    <div v-else>
      Loading timeline...
    </div>
    <sui-accordion exclusive>
      <div v-for="table in tables" :key="table.name">
        <sui-accordion-title>
          <h2><sui-icon name="dropdown" /> {{ table.title }}</h2>
        </sui-accordion-title>
        <sui-accordion-content>
          <historical-tab-table
            searchType="parcel_number"
            :searchToMatch="parcelNumber"
            :table="table"
          />
        </sui-accordion-content>
      </div>
    </sui-accordion>
  </div>
</template>

<script>
import HistoricalTabTable from "@/components/HistoricalTabTable";
import { getTableInfo } from "@/api/singleTable";
import * as d3 from "d3";
import timeline from "@/vue-timeline-component/graph/timeline";

export default {
  name: "HistoricalPropertyTab",
  components: { HistoricalTabTable },
  props: {
    parcelNumber: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      timelineData: null,
      loading: true,
      tables: [
        { title: "Violations", name: "violations" },
        { title: "Complaints", name: "complaints" },
        { title: "Appeals", name: "appeals" },
        { title: "Case Investigations", name: "case_investigations" }
      ]
    };
  },
  methods: {
    loadTimelineData(timelineData) {
      d3.select("#timeline")
        .datum(timelineData)
        .call(
          timeline({
            widthResizable: true,
            allowZoom: false,
            margin: {
              top: 0,
              bottom: 30,
              left: 30,
              right: 30
            }
            //onEventClick: click
          })
        );
    }
  },
  created() {
    getTableInfo("real_estate_transfers", "parcel_number", this.parcelNumber)
      .then(data => {
        if ("results" in data) {
          const timelineData = [];
          let prevEndDate = null;
          let lastGrantees = null;
          let sortedData = data.results.rows;
          sortedData.sort((a, b) => (a.receipt_date > b.receipt_date ? 1 : -1));
          sortedData = sortedData.filter(
            a =>
              a.document_type === "DEED" ||
              a.document_type === "DEED SHERIFF" ||
              a.document_type === "DEED OF CONDEMNATION" ||
              a.document_type === " DEED LAND BANK"
          );
          for (let i in sortedData) {
            let row = sortedData[i];
            row.name = row.grantors;
            if (i == 0) {
              row.start = new Date(
                row.year_built !== "0000" ? row.year_built : row.receipt_date
              );
            } else {
              row.start = new Date(Date.parse(prevEndDate));
            }
            row.end = new Date(Date.parse(row.receipt_date));
            prevEndDate = row.end;
            lastGrantees = row.grantees;
            let output = {
              name: row.name,
              start: row.start,
              end: row.end
            };
            timelineData.push(output);
          }
          timelineData.push({
            name: lastGrantees,
            start: prevEndDate,
            end: new Date()
          });
          this.timelineData = timelineData;
          this.loading = false;
          return timelineData;
        }
      })
      .then(timelineData => {
        this.loadTimelineData(timelineData);
      });
  }
};
</script>
