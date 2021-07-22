<template>
  <div>
    <h2>{{ mailingStreet }}</h2>
    This is crowd-sourced information keyed on the mailing street
    <sui-container>
      <div v-for="(bioResult, i) in bioResults" :key="i">
        <h2 is="sui-header">Entry {{ i }}</h2>
        <div v-for="(val, key) in bioResult" :key="key">
          <p v-if="key === 'link_to_owner_website'">
            <b>{{ key }}:</b><a :href="val" target="_blank">{{ val }}</a>
          </p>
          <p v-if="key === 'links_to_sources'">
            <b>{{ key }}</b
            ><br />
            <span v-for="(link, key2) in val.split(';')" :key="key2">
              - <a :href="link">{{ link }}</a
              ><br />
            </span>
          </p>
          <p v-else>
            <b>{{ key }}:</b>{{ val }}
          </p>
        </div>
      </div>
    </sui-container>
    <iframe
      class="airtable-embed"
      :src="airTableUrl"
      frameborder="0"
      onmousewheel=""
      width="100%"
      height="533"
      style="background: transparent; border: 1px solid #ccc;"
    ></iframe>
  </div>
</template>

<script>
import { getBioTableInfo } from "@/api/singleTable";

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
      airTableUrl:
        "https://airtable.com/embed/shrAacunffP2mP3PC?backgroundColor=orange&prefill_mailing_street=" +
        this.mailingStreet
    };
  },
  methods: {},
  created() {
    getBioTableInfo(this.mailingStreet).then(data => {
      this.bioResults = data.results;
    });
  }
};
</script>
