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
      const parcelNumber = selection["description"];
      this.$router.push("/property/" + parcelNumber);
    }
  }
};
</script>
