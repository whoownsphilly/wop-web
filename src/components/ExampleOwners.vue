<template lang="html">
  <sui-card-group :items-per-row="3">
    <sui-card>
      <sui-card-content>
        <a href="/#/owner/14%20WA%20PARTNERS%20LP">
          <sui-card-header>Pearl Properties</sui-card-header>
        </a>
        <sui-card-meta>110 S 19th St Suite 300</sui-card-meta>
        <sui-card-description>
          Example description.
        </sui-card-description>
      </sui-card-content>
      <sui-card-content extra>
        <sui-icon name="sitemap" /> N Properties
      </sui-card-content>
    </sui-card>
  </sui-card-group>
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
