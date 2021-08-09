<template lang="html">
  <sui-search action="search category" @select="select" fluid ref="searchBar">
    <template v-slot:input="{ props, handlers }">
      <div v-if="$siteMode.mode !== 'basic'">
        Search By:
        <sui-button
          size="tiny"
          data-tooltip="Search by owner or address"
          data-position="top center"
          attached="left"
          :color="searchType === 'addressOrOwner' ? 'green' : 'grey'"
          v-on:click="searchType = 'addressOrOwner'"
          >Owner or Address</sui-button
        >
        <sui-button
          size="tiny"
          attached="right"
          :color="searchType === 'mailingAddress' ? 'green' : 'grey'"
          data-tooltip="Search by mailing address"
          data-position="top center"
          v-on:click="searchType = 'mailingAddress'"
          >Owner Mailing Address</sui-button
        >
        <sui-divider hidden />
      </div>
      <sui-input
        size="massive"
        v-bind="props"
        v-on:blur="handlers.blur"
        v-on:input="handlers.input"
        v-on:focus="handlers.focus"
        v-model="selection"
        icon="search"
        :placeholder="searchBarPlaceholder"
        focus
        fluid
      />
    </template>
  </sui-search>
</template>

<script>
export default {
  name: "SearchBar",
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
      if (selection_type === "location") {
        const parcelNumber = selection["description"];
        this.$router.push("/property/" + parcelNumber);
      } else if (selection_type === "owner") {
        const owner = selection["description"];
        this.$router.push("/owner/" + owner);
      } else if (selection_type === "mailing-address") {
        const mailing_street = selection["description"];
        this.$router.push("/mailing_address/" + mailing_street);
      }
    }
  }
};
</script>
