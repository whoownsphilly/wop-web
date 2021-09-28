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
          >Owner or Location</sui-button
        >
        <sui-button
          size="tiny"
          attached="right"
          :color="searchType === 'mailingAddress' ? 'green' : 'grey'"
          data-tooltip="Search by mailing address"
          data-position="top center"
          v-on:click="searchType = 'mailingAddress'"
          >Owner's Mailing Address</sui-button
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
    // This is triggered when clicking on the selection, the populating of the
    // auto-complete itself happens due to an api call that is defined in main.js
    // due to the way that semantic-ui-vue's search bar requires.
    select(selection) {
      // Used the url param to pass the selection type (part of the search bar)
      const selectionIndex = selection["url"];
      let selectedResult = this.$store.state.searchResults[selectionIndex];

      // Save the selection to vuex so it can be referenced later.
      this.$store.dispatch("updateSelectedResult", selectedResult);

      let selectedParcelNumber = selectedResult["parcel_number"];
      this.$router.push("/property/" + selectedParcelNumber);
      /*
      if (selection_type === "location_unit") {
        const parcelNumber = selection["description"];
        this.$router.push("/property/" + parcelNumber);
      } else if (selection_type === "owner") {
        const owner = selection["description"];
        this.$router.push("/owner/" + owner);
      } else if (selection_type === "full_mailing_address") {
        //title is mailing street, description is mailing address
        const mailing_street = selection["title"];
        const mailing_address_1 = selection["description"];
        this.$router.push(
          "/mailing_address/" + mailing_street + "|" + mailing_address_1
        );
      }
      */
    }
  }
};
</script>
