<template>
  <div class="dashboard">
    <p>
      The city has many datasets available through
      <a
        href="https://www.opendataphilly.org/organization/city-of-philadelphia"
        target="_blank"
        >Open Data Philly</a
      >. They make these accessible through a service called Carto, which allows
      people to query the data through SQL using the
      <a href="https://carto.com/developers/sql-api/" target="_blank"
        >Carto SQL API</a
      >. This is really useful, allowing for full SQL queries (Postgres and
      PostGIS) including joins across tables. However, it still requires the use
      of a web request.
    </p>
    <p>
      This page allows anyone to directly write SQL, and receive the results in
      a searchable, downloadable format. This can be used for any dataset that
      is in Open Data Philly's Carto system.
    </p>
    <p>
      Feel free to explore the data. Note that any query that is executed gets
      attached to the URL, so if you want to share a query, simply execute it
      and then share the link at the top of the browser page. Anyone who goes to
      that link will have the same exact query executed.
    </p>
    <p>
      Note that these queries are real-time. If data changes in the city's
      databases, that means the results will change. So make sure to download
      any data that may be time-sensitive.
    </p>
    <sui-form>
      <sui-form-field>
        <label>Query</label>
        <textarea placeholder="Enter query here" v-model="query"></textarea>
      </sui-form-field>
    </sui-form>
    <sui-button :loading="loading" @click="executeQuery"
      >Execute Query</sui-button
    >
    <sui-divider />
    <div v-if="loading">
      <sui-dimmer active inverted>
        <sui-loader content="Executing the query" />
      </sui-dimmer>
    </div>
    <div v-else-if="error">
      {{ error }}
    </div>
    <div v-else>
      <data-table :rows="rows" :columns="columns" title="Query Results" />
    </div>
  </div>
</template>

<script>
import DataTable from "@/components/ui/DataTable";
import { format } from "sql-formatter";
export default {
  name: "ExplorePage",
  components: { DataTable },
  data() {
    return {
      rows: [],
      query: format(this.$route.query.q || ""),
      loading: false,
      error: null,
      columns: [],
    };
  },
  computed: {
    queryForUrl() {
      let queryNoComments = [];
      this.query.split("\n").forEach(function(x) {
        if (!x.trim().startsWith("--")) {
          console.log(x);
          queryNoComments.push(x);
        }
      });
      return queryNoComments
        .join("\n")
        .replace(/\n/g, " ")
        .replace(/\s\s+/g, " ");
    },
  },
  methods: {
    executeQuery(click, updateRoute = true) {
      this.loading = true;
      this.columns = [];
      this.rows = [];
      const url = `https://phl.carto.com/api/v2/sql?q=${encodeURIComponent(
        this.queryForUrl
      )}`;
      fetch(url, {
        method: "GET",
      })
        .then((response) => {
          if (updateRoute === true) {
            this.$router.push({
              query: Object.assign({}, this.$route.query, {
                q: this.query,
              }),
            });
          }
          return response.json();
        })
        .then((response_json) => {
          this.loading = false;
          this.error = null;
          if ("error" in response_json) {
            this.error = response_json["error"][0];
          } else {
            Object.keys(response_json["fields"]).forEach((row) => {
              this.columns.push({ label: row, field: row });
            });
            this.rows = response_json["rows"];
            console.log(this.query, updateRoute);
          }
        });
    },
  },
  created() {
    if (this.query.length > 0) {
      this.executeQuery(null, false);
    }
  },
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
