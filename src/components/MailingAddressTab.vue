<template>
  <div>
    <h2> {{ mailingStreet }}</h2>
    Mailing Address Information
  </div>
</template>

<script>

import { getBioTableInfo } from '@/api/singleTable'

export default {
  name: "HistoricalCrowdSourcedTab",
  props: {
      mailingStreet: {
          type: String,
          required: true
      }
  },
  data() {
    return {
        bioResults: [],
        airTableUrl: "https://airtable.com/embed/shrAacunffP2mP3PC?backgroundColor=orange&prefill_mailing_street=" + this.mailingStreet,
    }
  },
  created() {
      getBioTableInfo(this.mailingStreet).then(data => {
        this.bioResults = data.results
      });
  }
};
</script>
