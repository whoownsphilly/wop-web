<template>
  <div>
    <data-table :rows="rowsObject" :columns="columnObject" :title="title" />
  </div>
</template>

<script>
import DataTable from "@/components/ui/DataTable";
export default {
  name: "SingleColumnDataTable",
  components: {
    DataTable
  },
  props: {
    rows: {
      type: Array,
      required: true
    },
    title: {
      type: String
    }
  },
  computed: {
    columnObject() {
      return [{ label: this.title, field: "title" }];
    },
    rowsObject() {
      const title = this.title;
      title; // hack to get around linter that gets mad it doesnt get used
      return this.rows.map(val => {
        return { title: val };
      });
    }
  }
};
</script>
