<template>
  <div class="home">
    <div>
      <p>
        Enter a <b>Philly address</b> or <b>landlord's name</b>. Find out who owns what in Philly, what else they might own in the city, and information about their properties.
      </p>
      <p>
        <b>Is the address not showing up?</b> Search for the address on  <a href="https://atlas.phila.gov">atlas.phila.gov</a> to see how the City formats addresses and owner names. We try our best to match addresses to the City’s format, but sometimes the City formats addresses in ways we can't detect.
      </p>
    </div>
    <sui-divider hidden />
    <search-bar />
    <sui-divider hidden />
    or view sample owner portfolios...
    <ExampleOwners />
    <cookie-law theme="dark-lime">
      <div slot="message">
        The volunteers who contributed to this website make absolutely no
        guarantees as to the currency, accuracy, completeness, or quality of the
        information and data. No organization, group, or volunteer assumes any
        liability for the currency, accuracy, completeness, or quality of the
        information or data. The User assumes all responsibility and risk for
        the use of this site.
      </div>
    </cookie-law>
  </div>
</template>

<script>
// @ is an alias to /src

import SearchBar from "@/components/page/home/SearchBar";
import ExampleOwners from "@/components/page/home/ExampleOwners";
import CookieLaw from "vue-cookie-law";

export default {
  name: "Home",
  components: {
    SearchBar,
    ExampleOwners,
    CookieLaw
  }
};
</script>
<style>
.home {
  padding: 50px;
}
</style>
