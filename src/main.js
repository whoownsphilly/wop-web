import Vue from "vue";
import App from "./App.vue";
import SuiVue from "semantic-ui-vue";
import router from "./router";
import VueGoodTablePlugin from 'vue-good-table';
import ToggleSwitch from 'vuejs-toggle-switch'

// import the styles
import "semantic-ui-css/semantic.min.css";
import 'vue-good-table/dist/vue-good-table.css'
import 'leaflet/dist/leaflet.css';
// Fix marker issue with Leaflet
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
// import store
import store from './store/store'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

Vue.config.productionTip = false;

// add plugins
Vue.use(SuiVue);
Vue.use(VueGoodTablePlugin);
Vue.use(ToggleSwitch);

Vue.prototype.$siteMode = Vue.observable({mode: 'basic'})

new Vue({
  router,
    store,
  provide: {
    // Needed due to how semantic-ui-vue search bar works
    sui: {
      api: {
        base: process.env.VUE_APP_DJANGO_URL,
        api: {
            //"search category": "/api/v1/autocomplete?startswith_str={value}"
            "search category": "/api/v1/autocomplete?startswith_str={value}"
        },
        onSelect() {return false},
        onResponse(response) {
          console.log("api hit")
          store.dispatch('updateSearchResults',response.results);
          let searchBarResults = []
          response.results.forEach((result, index) => {
            // This translates the results into the required data format
              // for the search bar
                searchBarResults.push({"url": index.toString(), 
                    "description": result['description'], 
                    "title": result['location_unit'],
                })

          })
          // let searchResults = response.results
          return searchBarResults;
        }
      }
    }
  },
  render: h => h(App)
}).$mount("#app");
