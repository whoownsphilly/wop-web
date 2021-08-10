<template>
  <div>
    <sui-container>
    <p>This is crowd-sourced information keyed on the mailing street
    and currently contains <b>{{ bioResults.length }}</b> existing results.</p>
      <div v-for="(bioResult, i) in bioResults" :key="i">
        <BioResult :bioResult="bioResult" :index="i"/>
            <sui-divider />

      </div>
    </sui-container>
    <sui-accordion>
        <sui-accordion-title>
          <h2><sui-icon name="dropdown" /> Submit your own information</h2>
        </sui-accordion-title>
        <sui-accordion-content>
        <iframe
          class="airtable-embed"
          :src="airTableUrl"
          frameborder="0"
          onmousewheel=""
          width="100%"
          height="533"
          style="background: transparent; border: 1px solid #ccc;"
        />
        </sui-accordion-content>
    </sui-accordion>
  </div>
</template>

<script>
import { getBioTableInfo } from "@/api/singleTable";
import BioResult from "@/components/BioResult";

export default {
  name: "HistoricalCrowdSourcedTab",
  components: {
      BioResult
},
  props: {
    mailingStreet: {
      type: String,
      required: true
    },
    mailingAddress1: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      bioResults: [],
      airTableUrl:
        "https://airtable.com/embed/shrAacunffP2mP3PC?backgroundColor=orange&prefill_mailing_street=" +
        this.mailingStreet
    };
  },
  methods: {},
  created() {
    getBioTableInfo(this.mailingStreet, this.mailingAddress1).then(data => {
      this.bioResults = data.results;
    });
  }
};
</script>
