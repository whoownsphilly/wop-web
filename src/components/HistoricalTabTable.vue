<template>
  <div v-if="loading">
    Loading table data...
  </div>
  <div v-else>
    <vue-good-table
      :columns="columns"
      :rows="rows"
      :search-options="{
        enabled: true,
        trigger: 'enter',
        skipDiacritics: true,
        placeholder: 'Search this table'
      }"
      :pagination-options="{
        enabled: true,
        mode: 'records',
        perPage: 5,
        position: 'top',
        perPageDropdown: [10, 20],
        dropdownAllowAll: true,
        setCurrentPage: 1,
        nextLabel: 'next',
        prevLabel: 'prev',
        rowsPerPageLabel: 'Rows per page',
        ofLabel: 'of',
        pageLabel: 'page', // for 'pages' mode
        allLabel: 'All'
      }"
    />
  </div>
</template>

<script>
import { getTableInfo } from "@/api/singleTable";

export default {
  name: "HistoricalTabTable",
  props: {
    searchType: {
      type: String,
      required: true
    },
    searchToMatch: {
      type: String,
      required: true
    },
    tableName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      columns: [],
      rows: []
    };
  },
  created() {
    getTableInfo(this.tableName, this.searchType, this.searchToMatch).then(
      data => {
        if ("results" in data) {
          this.columns = data.results.columns;
          this.rows = data.results.rows;
        }
        this.loading = false;
      }
    );
  }
};
</script>
