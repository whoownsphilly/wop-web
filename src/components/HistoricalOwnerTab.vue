<template>
  <div>
    <span v-for="ownerName in ownersList" :key="ownerName.owner_name">
        <sui-button
        :content="ownerName.owner_name"
            toggle
            :active="isActive[ownerName.owner_name]"
            @click="changeActiveOwners"
      />
    </span>
    <div v-if="timelineData">
        <vue-timeline :data="timelineDataForGraph"></vue-timeline>
    </div>
    <div v-if="loadTables">
        <div v-for="table in tables" :key="table.name">
          <h2> {{table.title }}</h2>
          <historical-tab-table searchType="owner" :searchToMatch="owner" :tableName="table.name"/>
        </div>
    </div>
  </div>
</template>

<script>
import HistoricalTabTable from '@/components/HistoricalTabTable'
import { getOwnersTimelineTableInfo } from '@/api/singleTable'
import VueTimeline from "vue-timeline-component"

export default {
  name: "HistoricalOwnerTab",
  components: {HistoricalTabTable, VueTimeline},
  props: {
      owner: {
          type: String,
          required: true
      }
  },
  data() {
    return {
        loadTables: false,
        timelineData: null,
        ownersList: [],
        isActive: {},
        isActiveA: false,
        tables: [
            {"title": "Violations", "name": "violations"},
            {"title": "Complaints", "name": "complaints"},
            {"title": "Appeals", "name": "appeals"},
            {"title": "Case Investigations", "name": "case_investigations"},
        ],
    }
  },
  computed: {
      timelineDataForGraph() {
          // Temporary
          return this.timelineData.slice(0, 5)
    },
},
  methods: {
      changeActiveOwners(thisButton) {
          const thisButtonName = thisButton.srcElement.innerText;
          console.log(thisButtonName)
          this.isActive[thisButtonName] = !this.isActive[thisButtonName]
          this.isActive.__ob__.dep.notify() //I know this is hacky but I'm learning.
      }
  },
  created() {
      getOwnersTimelineTableInfo(this.owner).then(data => {
          const timelineData = []
          this.ownersList = data.owners_list
          for(let i in data.owners_list){
              this.isActive[data.owners_list[i].owner_name] = true
          }
          for(let i in data.owner_timeline){
              let row = data.owner_timeline[i]
              row.name = row.location + " " + (row.unit || "")
              row.start = new Date(Date.parse(row.start_dt))
              row.end = new Date(Date.parse(row.end_dt) || Date())
              let output = {
                  name: row.name,
                  start: row.start,
                  end: row.end,
              }
              timelineData.push(output)

            }
            this.timelineData = timelineData
          });
  },
};
</script>
