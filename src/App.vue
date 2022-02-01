<template>
  <div id="app">
    <div id="nav">
      <b>Who Owns Philly?</b><br />
      <router-link to="/">Home</router-link> |
      <router-link to="/take-action"
        ><b>Click Here to Take Action</b></router-link
      >
      |
      <router-link to="/about"><b>About</b></router-link>
    </div>
    <router-view />
  </div>
</template>

<script>
import Vue from "vue";

export default {
  name: "App",
  methods: {
    setSiteMode(thisSiteMode) {
      Vue.prototype.$siteMode.mode = thisSiteMode;
    },
  },
  created() {
    document.title = "Who Owns Philly?";
    this.setSiteMode(this.$route.query.siteMode || "basic");
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}

#nav {
  text-align: center;
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
#advanced-selector {
  float: right;
  display: inline-block;
}
</style>
