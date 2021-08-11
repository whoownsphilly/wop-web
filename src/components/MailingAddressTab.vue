<template>
  <div>
    Mailing Address Information
  </div>
</template>

<script>
import { getBioTableInfo } from "@/api/singleTable";

export default {
  name: "HistoricalCrowdSourcedTab",
  props: {
    mailingAddress1: {
      type: String,
      required: true
    },
    mailingStreet: {
      type: String,
      required: true
    }
  },
  computed: {},
  data() {
    return {
      bioResults: [],
      airTableUrl:
        "https://airtable.com/embed/shrAacunffP2mP3PC?backgroundColor=orange&prefill_mailing_street=" +
        this.mailingStreet
    };
  },
  created() {
    getBioTableInfo(this.mailingStreet, this.mailingAddress1).then(data => {
     console.log(data.results)
      this.bioResults = data.results;
    });
  }
};
</script>
