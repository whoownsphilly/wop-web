<template>
  <div>
    <h2> {{ mailingStreet }}</h2>
    This is crowd-sourced information keyed on the mailing street
    <sui-container>
        <div v-for="bioResult, i in bioResults" :key="i">
          <h2 is="sui-header">Entry {{ i }}</h2>
          <div v-for="(val, key) in bioResult" :key="key">
            <p v-if="key === 'link_to_owner_website'">
                <b>{{ key }}:</b>{{ linkifyTheHtml(val) }}
            </p>
            <p v-else>
                <b>{{ key }}:</b>{{ linkifyTheHtml(val) }}
            </p>
          </div>
        </div>
    </sui-container>
    <iframe class="airtable-embed" :src="airTableUrl" frameborder="0" onmousewheel="" width="100%" height="533" style="background: transparent; border: 1px solid #ccc;"></iframe>
  </div>
</template>

<script>

import { getBioTableInfo } from '@/api/singleTable'
import linkifyHtml from 'linkifyjs/html';

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
  methods: {
      linkifyTheHtml(val) {
          return linkifyHtml("" + val)
      }
  },
  created() {
      getBioTableInfo(this.mailingStreet).then(data => {
        this.bioResults = data.results
      });
  }
};
</script>
