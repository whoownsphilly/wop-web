<template>
  <div>
    <sui-container>
      <p v-if='bioResults.length > 0'>
        The following information was developed and maintained by volunteers. The information includes data from secondary sources, which are not guaranteed to be checked for accuracy and do not necessarily reflect the opinions of any organization or group. No organization, group, or volunteer endorses or accepts responsibility over any external sites that may be linked in this information. The volunteers who contributed to this information make absolutely no guarantees as to the currency, accuracy, completeness, or quality of information written and/or archived on the website, and no organization, group, or volunteer assumes any liability for the currency, accuracy, completeness, or quality of information written and/or archived on the website. The inclusion of names, links and other references is purely on the basis of their relevance to the information.

        It currently contains <b>{{ bioResults.length }}</b> existing results.
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
    }
  },
  created() {
    getBioTableInfo(this.mailingStreet, this.mailingAddress1).then(data => {
      this.bioResults = data.results;
    });
  }
};
</script>
