<template lang="html">
      <div class="propertyHeader">
        <sui-statistic horizontal>
          <sui-statistic-value>{{
            propertyString
          }}</sui-statistic-value>
          <sui-statistic-label> is likely owned by</sui-statistic-label>
        </sui-statistic>
        <sui-statistic horizontal>
          <sui-statistic-value>
            <span v-tooltip.bottom="propertySourceString"
              >{{ latestOwnerString }}<sup>*</sup></span
            ></sui-statistic-value
          >
        </sui-statistic>
        <br>
        <span v-if="ownerByMailingAddress">
            <sui-statistic horizontal>
              <sui-statistic-label> and managed by </sui-statistic-label>
              <sui-statistic-value>
              <span v-if="ownerByMailingAddress.url">
                  <a :href='ownerByMailingAddress.url' target="_blank">{{ ownerByMailingAddress.name }}</a>
              </span>
              <span v-else>
              {{ ownerByMailingAddress.name }}
              </span>
              </sui-statistic-value>
              </sui-statistic>
          </span>
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
    ownerByMailingAddress: {
        type: Object,
    },
    propertySourceString: {
      type: String,
      required: true
    },
  },
  computed: { },
  methods: { }
};
</script>
<style>
.propertyHeader {
  text-align: center;
  font-size: 16px;
}
</style>
