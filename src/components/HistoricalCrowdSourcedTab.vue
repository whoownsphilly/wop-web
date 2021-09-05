<template>
  <div>
    <sui-container>
      <p>
        The following crowd-sourced information is keyed on the mailing street and
        currently contains <b>{{ bioResults.length }}</b> existing results. 
      </p>
      <div v-for="(bioResult, i) in bioResults" :key="i">
        <BioResult :bioResult="bioResult" :index="i" />
        <sui-divider />
      </div>
    </sui-container>
        <sui-button @click.native="toggle">Submit your own information</sui-button>

    <sui-modal v-model="modalOpen">
      <sui-modal-header>Submit form</sui-modal-header>
      <sui-modal-content scrolling image>
        <iframe
          class="airtable-embed"
          :src="airTableUrl"
          frameborder="0"
          onmousewheel=""
          width="100%"
          height="533"
          style="background: transparent; border: 1px solid #ccc;"
        />
      </sui-modal-content>
      <sui-modal-actions>
        <sui-button positive @click.native="toggle">
          Ok
        </sui-button>
      </sui-modal-actions>
    </sui-modal>
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
      modalOpen: false,
      bioResults: [],
      airTableUrl:
        "https://airtable.com/embed/shrAacunffP2mP3PC?backgroundColor=orange&prefill_mailing_street=" +
        this.mailingStreet
    };
  },
  methods: {
   toggle() {
      this.modalOpen = !this.modalOpen;
    },
  },
  created() {
    getBioTableInfo(this.mailingStreet, this.mailingAddress1).then(data => {
      this.bioResults = data.results;
    });
  }
};
</script>
