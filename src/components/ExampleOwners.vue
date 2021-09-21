<template lang="html">
  <sui-card-group :items-per-row="3">
    <sui-card>
      <sui-card-content>
        <a href="/#/property/032022200">
          <sui-card-header>Odin Properties</sui-card-header>
        </a>
        <sui-card-meta>1200 Callowhill St Suite 300</sui-card-meta>
        <sui-card-description>
            Odin Properties was founded in 2009 by real estate investor Philip Balderston. Balderston left Tower Investments (Bart Blatstein) after the foreclosure crisis to buy distressed properties in Philadelphia.
        </sui-card-description>
      </sui-card-content>
      <sui-card-content extra>
        <sui-icon name="sitemap" /> ~80 Properties
      </sui-card-content>
    </sui-card>
    <sui-card>
      <sui-card-content>
        <a href="/#/property/871288650">
          <sui-card-header>Allan Domb Realty</sui-card-header>
        </a>
        <sui-card-meta>1845 Walnut St Suite 2200</sui-card-meta>
        <sui-card-description>
        1845 Walnut is a large office building on Rittenhouse Square with many suites, and several suites are associated with realty companies...
        </sui-card-description>
      </sui-card-content>
      <sui-card-content extra>
        <sui-icon name="sitemap" /> ~800 Properties
      </sui-card-content>
    </sui-card>
    <sui-card>
      <sui-card-content>
        <a href="/#/property/888058983">
          <sui-card-header>Pearl Properties</sui-card-header>
        </a>
        <sui-card-meta>110 S 19th St Suite 300</sui-card-meta>
        <sui-card-description>
          Pearl Properties works in real estate development, construction, residential leasing, and property management. Multiple LLCs receive mail to Pearl Properties' office, including 14 WA Partners LP, associated with 1401 Walnut - Pearl Apartments.
        </sui-card-description>
      </sui-card-content>
      <sui-card-content extra>
        <sui-icon name="sitemap" /> ~50 Properties
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
