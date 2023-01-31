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
        perPage: 20,
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
        <a :href="generateCSVUrl" :download="filename" target="_blank"
          >Download this table</a
        >
      </div>
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'link'">
          <a target="_blank" :href="props.row.link">Click Here</a>
        </span>
        <span v-else>
          {{ props.formattedRow[props.column.field] }}
        </span>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
export default {
  name: "DataTable",
  props: {
    rows: {
      type: Array,
      required: true
    },
    title: {
      type: String
    }
  },
  data() {
    return {};
  },
  computed: {
    filename() {
      return (this.title || "download") + ".csv";
    },
    columns() {
      if (this.rows.length > 0) {
        return Object.keys(this.rows[0]).map(col => {
          let fieldType = isNaN(this.rows[0][col]) ? "string" : "number";
          return { label: col, field: col, type: fieldType };
        });
      } else {
        return [];
      }
    },
    generateCSVUrl() {
      let colNames = this.columns.map(col => {
        return col.label;
      });
      let csv = colNames.join(",") + "\n";
      this.rows.forEach(row => {
        let outputRow = [];
        colNames.forEach(col => {
          outputRow.push(row[col]);
        });
        csv += outputRow.join(",") + "\n";
      });
      return "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
    }
  }
};
</script>
