<template lang="html">
  <sui-card-group :items-per-row="3">
    <sui-card>
      <sui-card-content>
        <a href="/#/property/011455700">
          <sui-card-header>Odin Properties</sui-card-header>
        </a>
        <sui-card-meta>1200 Callowhill St Suite 300</sui-card-meta>
        <sui-card-description>
          Example description.
        </sui-card-description>
      </sui-card-content>
      <sui-card-content extra>
        <sui-icon name="sitemap" /> N Properties
      </sui-card-content>
    </sui-card>
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
  name: "ExampleOwners",
  data() {
    return {};
  },
  methods: {}
};
</script>
