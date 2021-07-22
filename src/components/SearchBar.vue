<template lang="html">
  <sui-search action="search category" @select="select" fluid ref="searchBar">
    <template v-slot:input="{ props, handlers }">
      <sui-input
        size="massive"
        v-bind="props"
        v-on:blur="handlers.blur"
        v-on:input="handlers.input"
        v-on:focus="handlers.focus"
        v-model="selection"
        icon="search"
        placeholder="Search address or owner...."
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
      selection: null
    };
  },
  methods: {
    select(selection) {
      // Used the url param to pass the selection type (part of the search bar)
      const selection_type = selection["url"]
      if(selection_type === "location"){
          const parcelNumber = selection["description"];
          this.$router.push("/property/" + parcelNumber);
      }
      else if(selection_type === "owner"){
          const owner = selection["description"];
          this.$router.push("/owner/" + owner)
      }
      else if(selection_type === "mailing-address"){
          const mailing_street = selection["description"];
          this.$router.push("/mailing_address/" + mailing_street)
      }
    }
  }
};
</script>
