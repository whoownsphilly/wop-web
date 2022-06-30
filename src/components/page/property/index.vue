<template>
  <div>
    <sui-grid>
      <sui-grid-row>
        <sui-grid-column :width="6">
          <div style="height:600px">
            <vue-iframe :src="streetViewLink" />
          </div>
        </sui-grid-column>
        <sui-grid-column :width="10">
          <property-basics :parcelNumber="parcelNumber" />
          <router-link to="/take-action" class="ui button positive" tag="button"
            >Click here to take action!</router-link
          >
        </sui-grid-column>
      </sui-grid-row>
    </sui-grid>
  </div>
</template>

<script>
import PropertyBasics from "@/components/page/property/PropertyBasics";
export default {
  name: "PropertyIndex",
  components: { PropertyBasics },
  props: {
    parcelNumber: {
      type: String,
      required: true
    },
    streetViewLink: {
      type: String,
      required: true
    }
  },
  methods: {},
  created() {}
};
</script>
<style>
.ui.accordion .title:not(.ui) {
  font-size: 2em;
}
</style>
