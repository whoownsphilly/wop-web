<template>
  <div class="property">
    <sui-container text>
      <h2>{{ owner }}</h2>
      <historical-owner-tab :owner="owner" />
    </sui-container>
  </div>
</template>

<script>
import HistoricalOwnerTab from "@/components/page/owner";

export default {
  name: "Property",
  components: {
    HistoricalOwnerTab
  },
  data() {
    return {
      result: null,
      resultLoaded: false
    };
  },
  computed: {
    owner() {
      return this.$route.params.ownerName;
    }
  },
  created() {}
};
</script>
