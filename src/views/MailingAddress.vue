<template>
  <div class="mailing-address">
    <sui-container text>
      <h2>{{ mailingStreet }} {{ mailingAddress1 }}</h2>
    </sui-container>
    <historical-crowd-sourced-tab
      :mailingStreet="mailingStreet"
      :mailingAddress1="mailingAddress1"
    />
  </div>
</template>

<script>
import HistoricalCrowdSourcedTab from "@/components/page/mailing_address";

export default {
  name: "MailingAddress",
  components: {
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
      return this.$route.params.fullMailingAddress.split("|")[0];
    },
    mailingAddress1() {
      return this.$route.params.fullMailingAddress.split("|")[1];
    }
  },
  created() {}
};
</script>
