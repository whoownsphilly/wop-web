<template>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader
        content="Finding All Related Owners (may take some time)..."
      />
    </sui-dimmer>
  </div>
  <div v-else>
    <h2>connected to {{ timelineData.length }} properties</h2>
    <sui-accordion exclusive>
      <sui-accordion-title>
        <h2>
          <sui-icon name="dropdown" />
          Owners ({{ ownersList.length }})
        </h2>
      </sui-accordion-title>
      <sui-accordion-content>
        <span v-for="ownerName in ownersList" :key="ownerName.owner_name">
          <sui-button
            :content="ownerName.owner_name"
            toggle
            :active="isActive[ownerName.owner_name]"
            @click="changeActiveOwners"
          />
        </span>
      </sui-accordion-content>
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
    <div v-if="timelineData && $siteMode.mode !== 'basic'">
      <vue-timeline :data="timelineDataForGraph"></vue-timeline>
    </div>
  </div>
</template>

<script>
import HistoricalTabTable from "@/components/ui/HistoricalTabTable";
import { getOwnersTimelineTableInfo } from "@/api/singleTable";
import VueTimeline from "@/vue-timeline-component/components/VueTimeline";

export default {
  name: "HistoricalOwnerTab",
  components: { HistoricalTabTable, VueTimeline },
  props: {
    owner: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      latLngs: [],
      highlightedLatLng: null,
      loading: true,
      loadTables: true,
      timelineData: null,
      ownersList: [],
      isActive: {},
      tables: [
        { title: "Violations", name: "violations" },
        { title: "Complaints", name: "complaints" },
        { title: "Appeals", name: "appeals" },
        { title: "Case Investigations", name: "case_investigations" }
      ]
    };
  },
  computed: {
    timelineDataForGraph() {
      return this.timelineData;
    }
  },
  methods: {
    changeActiveOwners(thisButton) {
      const thisButtonName = thisButton.srcElement.innerText;
      this.isActive[thisButtonName] = !this.isActive[thisButtonName];
      this.isActive.__ob__.dep.notify(); //I know this is hacky but I'm learning.
    }
  },
  async created() {
    // First get the lat lng for the selected property

    // Next get the owner timeline which is necessary for getting counts of
    // violations/complaints/etc.
    const data = await getOwnersTimelineTableInfo(this.owner);
    const timelineData = [];
    this.ownersList = data.owners_list;
    for (let i in data.owners_list) {
      this.isActive[data.owners_list[i].owner_name] = true;
    }
    for (let i in data.owner_timeline) {
      let row = data.owner_timeline[i];
      row.name = row.location + " " + (row.unit || "");
      row.start = new Date(Date.parse(row.start_dt));
      row.end = new Date(Date.parse(row.end_dt) || Date());
      let output = {
        name: row.name,
        start: row.start,
        end: row.end
      };
      timelineData.push(output);
      this.latLngs.push({ lat: row.lat, lng: row.lng });
    }
    // sort by newest to oldest
    timelineData.sort((a, b) => (a.start < b.start ? 1 : -1));
    this.timelineData = timelineData;
    this.loading = false;
  }
};
</script>
