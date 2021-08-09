<template>
  <div class="home">
    <div>
      <p>
        Enter a <b>Philly address</b> or <b>landlord's name</b> to find out who
        owns what in Philly what else they might own in the city, and any
        complaints, violations, real estate transactions, and active rental
        licenses associated with their properties.
      </p>
      <p>
        <b>Can't find the address?</b> Click
        <a href="https://atlas.phila.gov"> here</a> or
        <a href="https://phillypropertylookup.herokuapp.com">here</a> to see how
        the city formats addresses and owner names. We try our best to search in a similar way, but sometimes the city renames addresses in ways we can't detect.
      </p>
    </div>
    <sui-divider hidden />
    <SearchBar />
    <sui-divider hidden />
    <ExampleOwners />
  </div>
</template>

<script>
// @ is an alias to /src

import SearchBar from "@/components/SearchBar";
import ExampleOwners from "@/components/ExampleOwners";

export default {
  name: "Home",
  components: {
    SearchBar,
    ExampleOwners
  }
};
</script>
<style>
.home {
  padding: 50px;
}
</style>
