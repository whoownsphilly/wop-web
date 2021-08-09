<template>
  <div v-if="loading">
    <sui-dimmer active inverted>
      <sui-loader
        content="Finding All Related Owners (may take some time)..."
      />
    </sui-dimmer>
  </div>
  <div v-else>
    <sui-accordion exclusive>
      <leaflet-map :latLngs="latLngs" />
      <sui-accordion-title>
        <h2><sui-icon name="dropdown" />Edit Owner List</h2>
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
      <sui-accordion-title>
        <h2><sui-icon name="dropdown" />Timeline</h2>
      </sui-accordion-title>
      <sui-accordion-content> </sui-accordion-content>
      <div v-if="timelineData">
        <vue-timeline :data="timelineDataForGraph"></vue-timeline>
      </div>
      <div v-if="loadTables">
        <div v-for="table in tables" :key="table.name">
          <sui-accordion-title>
            <h2><sui-icon name="dropdown" /> {{ table.title }}</h2>
          </sui-accordion-title>
          <sui-accordion-content>
            <historical-tab-table
              searchType="owner"
              :searchToMatch="owner"
              :tableName="table.name"
            />
          </sui-accordion-content>
        </div>
      </div>
    </sui-accordion>
  </div>
</template>

<script>
import HistoricalTabTable from "@/components/HistoricalTabTable";
import LeafletMap from "@/components/LeafletMap";
import { getOwnersTimelineTableInfo } from "@/api/singleTable";
import VueTimeline from "@/vue-timeline-component/components/VueTimeline";

export default {
  name: "HistoricalOwnerTab",
  components: { HistoricalTabTable, VueTimeline, LeafletMap },
  props: {
    owner: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      latLngs: [],
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
      console.log(thisButtonName);
      this.isActive[thisButtonName] = !this.isActive[thisButtonName];
      this.isActive.__ob__.dep.notify(); //I know this is hacky but I'm learning.
    }
  },
  async created() {
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
