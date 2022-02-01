<template>
  <div>
    <sui-container>
      This page contains crowd-sourced information based on the mailing address
      of the property, as a way to group together any information about the
      entity that handles the taxes and other business mail for this property.
      This is typically a property manager. Fill out the form below to
      contribute any information you have about your property. Any entries will
      be manually checked to make sure they don't contain any revealing
      information, but remember that this information will be shared on this
      website with others so make sure there is nothing particularly
      identifying. If you have specific concerns and would like help with a
      landlord, it is best to instead contact one of the organizations on
      <router-link to="/take-action">page</router-link>.
      <h2>
        Information for properties with mailing address:
        {{ fullMailingAddress }}
      </h2>
      <p v-if="bioResults.length > 0">
        This currently contains <b>{{ bioResults.length }}</b> existing results.
        <sui-button
          circular
          icon="exclamation"
          @click.native="disclaimerToggle"
        />
        <sui-modal v-model="disclaimerOpen">
          <sui-modal-header
            >Crowd-Sourced Information Disclaimer</sui-modal-header
          >
          <sui-modal-content>
            <p>
              The following information was developed and maintained by
              volunteers. The information includes data from secondary sources,
              which are not guaranteed to be checked for accuracy and do not
              necessarily reflect the opinions of any organization or group. No
              organization, group, or volunteer endorses or accepts
              responsibility over any external sites that may be linked in this
              information. The volunteers who contributed to this information
              make absolutely no guarantees as to the currency, accuracy,
              completeness, or quality of information written and/or archived on
              the website, and no organization, group, or volunteer assumes any
              liability for the currency, accuracy, completeness, or quality of
              information written and/or archived on the website. The inclusion
              of names, links and other references is purely on the basis of
              their relevance to the information.
            </p>
          </sui-modal-content>
          <sui-modal-actions>
            <sui-button positive @click.native="disclaimerToggle">
              OK
            </sui-button>
          </sui-modal-actions>
        </sui-modal>
      </p>
      <p v-else>
        There is not yet any crowd-sourced information for this mailing address.
      </p>
      <div v-for="(bioResult, i) in bioResults" :key="i">
        <bio-result :bioResult="bioResult" :index="i" />
        <sui-divider />
      </div>
      <sui-button @click.native="toggle"
        >Submit your own information</sui-button
      >
    </sui-container>

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
import BioResult from "@/components/page/crowdSourced/BioResult";
import { getCrowdSourcedPageInfo } from "@/api/pages";

export default {
  name: "CrowdSourcedTab",
  components: {
    BioResult,
  },
  props: {
    parcelNumber: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      bioResults: [],
      fullMailingAddress: null,
      mailingStreet: null,
      modalOpen: false,
      disclaimerOpen: false,
    };
  },
  computed: {
    airTableUrl() {
      return (
        "https://airtable.com/embed/shrAacunffP2mP3PC?backgroundColor=orange&prefill_mailing_street=" +
        this.mailingStreet
      );
    },
  },
  methods: {
    toggle() {
      this.modalOpen = !this.modalOpen;
    },
    disclaimerToggle() {
      this.disclaimerOpen = !this.disclaimerOpen;
    },
  },
  created() {
    getCrowdSourcedPageInfo(this.parcelNumber).then((results) => {
      this.bioResults = results["results"];
      this.fullMailingAddress = results["full_mailing_address"];
      this.mailingStreet = results["query"]["mailing_street"];
    });
  },
};
</script>
