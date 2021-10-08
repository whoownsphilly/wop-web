<template>
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
</template>

<script>
import { getTableInfo } from "@/api/singleTable";

export default {
  name: "DataTable",
  props: {
    columns: {
      type: Object,
      required: true
    },
    rows: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      loading: true,
      columns: [],
      rows: []
    };
  },
};
</script>
