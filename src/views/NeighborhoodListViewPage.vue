<template>
  <div style="font-size: 18px">
    <div v-if="loading === false">
      <property-list :name="name" :propertyList="thisList" />
    </div>
    <div v-else>
      <sui-dimmer active inverted>
        <sui-loader content="Loading..." />
      </sui-dimmer>
    </div>
  </div>
</template>
<script>
import PropertyList from "@/components/page/neighborhoods/PropertyList";
import { getNeighborhoodsPageFromParcelNumbers } from "@/api/pages";

export default {
  name: "NeighborhoodListViewPage",
  data() {
    return {
      name: null,
      loading: false,
      thisList: []
    };
  },
  components: {
    PropertyList
  },
  created() {
    this.name = Object.keys(this.$route.query)[0];
    this.loading = true;
    getNeighborhoodsPageFromParcelNumbers(this.$route.query).then(
      results => (
        (this.thisList = results.saved_properties[this.name]),
        (this.loading = false)
      )
    );
  }
};
</script>
