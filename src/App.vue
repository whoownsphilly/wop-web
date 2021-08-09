<template>
  <div id="app">

    <div id="nav">
      <div id='advanced-selector'>
        <sui-button-group>
          <sui-button
            size="tiny"
            data-tooltip="Basic Mode"
            data-position="bottom right"
            :color="$siteMode.mode === 'basic'? 'green': 'grey'"
            @click="setSiteMode('basic')"
          >Tenants</sui-button>
          <sui-button size="tiny"
            :color="$siteMode.mode === 'advanced' ? 'green': 'grey'"
            data-tooltip="Advanced search and possibly unfinished features"
            data-position="bottom right"
            @click="setSiteMode('advanced')"
          >Researchers</sui-button>
          <sui-button size="tiny"
            :color="$siteMode.mode === 'beta' ? 'green': 'grey'"
            data-tooltip="Advanced search and possibly unfinished features"
            data-position="bottom right"
            @click="setSiteMode('beta')"
          >Beta</sui-button>
        </sui-button-group>
      </div>
      <b>Who Owns Philly?</b><br>
      <router-link to="/">Home</router-link> |
      <router-link to="/about"><b>Click Here to Take Action</b></router-link>
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
      Vue.prototype.$siteMode.mode = thisSiteMode
    },
  },
}
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
float:right;
display: inline-block
}
</style>
