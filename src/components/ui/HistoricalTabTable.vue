<template>
  <div>
    <sui-accordion-title>
      <h2>
        <sui-icon name="dropdown" v-if="$siteMode.mode !== 'basic'" />
        {{ table.title }} ({{ this.rows.length }})
      </h2>
    </sui-accordion-title>
    <sui-accordion-content>
      <vue-good-table
        :columns="columns"
        :rows="rows"
        :isLoading="loading"
        :search-options="{
          enabled: true,
          trigger: 'enter',
          skipDiacritics: true,
          placeholder: 'Search ' + table.name
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
    </sui-accordion-content>
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
    table: {
      type: Object,
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
    getTableInfo(this.table.name, this.searchType, this.searchToMatch).then(
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
