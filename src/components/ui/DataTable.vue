<template>
  <div>
  <vue-good-table
    :columns="columns"
    :rows="rows"
    :search-options="{
      enabled: true,
      trigger: 'enter',
      skipDiacritics: true,
      placeholder: 'Search...'
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
  ><div slot="table-actions">
    <a :href="generateCSVUrl" :download="filename" target="_blank">Download this table</a>
  </div>
  </vue-good-table>
  </div>
</template>

<script>

export default {
  name: "DataTable",
  props: {
    columns: {
      type: Array,
      required: true
    },
    rows: {
      type: Array,
      required: true
    },
    title: {
        type: String
    }
  },
  data() {
    return {
    };
  },
  computed: {
    filename() {
        return (this.title || "download") + ".csv"
    },
    generateCSVUrl() {
    let colNames = this.columns.map(col => {return col.label})
    let csv = colNames.join(",") + "\n"
    this.rows.forEach((row) => {
        let outputRow = []
        colNames.forEach((col) => { outputRow.push(row[col])})
        csv += outputRow.join(",") + "\n";
    });
    return "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
}
}
};
</script>
