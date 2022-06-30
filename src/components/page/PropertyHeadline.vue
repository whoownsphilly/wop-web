<template lang="html">
  <div class="propertyHeader">
    <sui-statistic horizontal>
      <sui-statistic-value>{{ propertyString }}</sui-statistic-value>
      <sui-statistic-label> is likely owned by</sui-statistic-label>
    </sui-statistic>
    <sui-statistic horizontal>
      <sui-statistic-value>
        {{ latestOwnerString }}
      </sui-statistic-value> </sui-statistic
    ><sup><info-modal modalName="propertyHeadline.ownerModalInfo"/></sup>
    <br />
    <!--
    <span v-if="mailingAddress">
      <sui-statistic horizontal>
        <sui-statistic-label> with mailing address </sui-statistic-label>
        <sui-statistic-value>
          {{ mailingAddress }}
        </sui-statistic-value>
      </sui-statistic>
    </span>
    -->
  </div>
</template>

<script>
export default {
  name: "PropertyHeadline",
  props: {
    propertyString: {
      type: String,
      required: true
    },
    latestOwnerString: {
      type: String,
      required: true
    },
    mailingAddress: {
      type: String
    },
    propertySourceString: {
      type: String,
      required: true
    }
  },
  components: {},
  computed: {},
  methods: {}
};
</script>
<style>
.propertyHeader {
  text-align: center;
  font-size: 16px;
}
</style>
