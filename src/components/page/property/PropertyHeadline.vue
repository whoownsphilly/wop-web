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
            {{ latestOwnerString }}
          </sui-statistic-value>
        </sui-statistic><sup><info-modal modalName="propertyHeadline.ownerModalInfo" /></sup>
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
import InfoModal from "@/components/ui/InfoModal";
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
  components: {
    InfoModal
  },
  computed: { 
      ownerModalInfo(){
          return "This is the modal for owners"
      }
  },
  methods: { }
};
</script>
<style>
.propertyHeader {
  text-align: center;
  font-size: 16px;
}
</style>
