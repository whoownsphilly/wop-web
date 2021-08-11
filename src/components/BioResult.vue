<template lang="html">
  <div>
    <h2>
      <a :href="bioResult.link_to_owner_website">{{
        bioResult.name_of_possible_owner
      }}</a>
    </h2>
    <p>Ownership Confidence: {{ bioResult.confidence }}/5</p>
    <p>{{ bioResult.bio_of_owner }}</p>
    <p>
      <b>Links to Sources:</b><br />
      <span
        v-for="(link, key2) in bioResult.links_to_sources.split(';')"
        :key="key2"
      >
        - <a :href="link">{{ link }}</a
        ><br />
      </span>
    </p>
    <div v-if="$siteMode.mode === 'beta'">
      <h2 is="sui-header">Entry {{ index }}</h2>
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
  </div>
</template>

<script>
export default {
  name: "BioResult",
  props: {
    bioResult: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      test: "abc",
      searchType: "addressOrOwner",
      selection: null
    };
  },
  computed: {
    searchBarPlaceholder() {
      let placeholder = "Search...";
      if (this.searchType === "addressOrOwner") {
        placeholder = "Search address or owner...";
      } else if (this.searchType === "mailingAddress") {
        placeholder = "Search mailing address...";
      }
      return placeholder;
    }
  },
  methods: {
    select(selection) {
      // Used the url param to pass the selection type (part of the search bar)
      const selection_type = selection["url"];
      if (selection_type === "location_unit") {
        const parcelNumber = selection["description"];
        this.$router.push("/property/" + parcelNumber);
      } else if (selection_type === "owner") {
        const owner = selection["description"];
        this.$router.push("/owner/" + owner);
      } else if (selection_type === "full_mailing_address") {
        //title is mailing street, description is amiling address
        const mailing_street = selection["title"];
        const mailing_address_1 = selection["description"];
        this.$router.push(
          "/mailing_address/" + mailing_street + "|" + mailing_address_1
        );
      }
    }
  }
};
</script>
