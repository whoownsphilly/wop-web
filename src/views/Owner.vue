<template>
  <div class="property">
    <sui-container text>
      <h2>{{ owner }}</h2>
      <historical-owner-tab :owner="owner" />
    </sui-container>
  </div>
</template>

<script>
import HistoricalOwnerTab from "@/components/HistoricalOwnerTab";

export default {
  name: "Property",
  components: {
    HistoricalOwnerTab
  },
  data() {
    return {
      owner: this.$route.params.ownerName,
      result: null,
      resultLoaded: false
    };
  },
  computed: {},
  created() {}
};
</script>
