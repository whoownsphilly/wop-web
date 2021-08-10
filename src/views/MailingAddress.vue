<template>
  <div class="mailing-address">
    <sui-container text>
      <h2>{{ mailingStreet }} {{ mailingAddress1 }}</h2>
      <mailing-address-tab :mailingStreet="mailingStreet" :mailingAddress1="mailingAddress1" />
    </sui-container>
  <historical-crowd-sourced-tab
    :mailingStreet="mailingStreet"
    :mailingAddress1="mailingAddress1"
  />
  </div>
</template>

<script>
import MailingAddressTab from "@/components/MailingAddressTab";
import HistoricalCrowdSourcedTab from "@/components/HistoricalCrowdSourcedTab";

export default {
  name: "MailingAddress",
  components: {
    MailingAddressTab,
    HistoricalCrowdSourcedTab
  },
  data() {
    return {
      result: null,
      resultLoaded: false
    };
  },
  computed: {
      mailingStreet() {
          return this.$route.params.fullMailingAddress.split('|')[0]
        },
        mailingAddress1() {
            return this.$route.params.fullMailingAddress.split('|')[1]
        }
    },
  created() {}
};
</script>
