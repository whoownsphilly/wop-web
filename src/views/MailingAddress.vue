<template>
  <div class="mailing-address">
    <sui-container text>
        <h2>{{ mailing_street }}</h2>
        <mailing-address-tab :mailing-street="mailing_street"/>
    </sui-container>
  </div>
</template>

<script>
import MailingAddressTab from '@/components/MailingAddressTab'

export default {
  name: "MailingAddress",
  components: {
      MailingAddressTab,
},
  data() {
    return {
      mailing_street: this.$route.params.mailingStreet,
      result: null,
      resultLoaded: false
    };
  },
  computed: {
  },
  created() {
  }
};
</script>
