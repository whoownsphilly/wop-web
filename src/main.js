import Vue from "vue";
import App from "./App.vue";
import SuiVue from "semantic-ui-vue";
import router from "./router";
import VueGoodTablePlugin from 'vue-good-table';

// import the styles
import "semantic-ui-css/semantic.min.css";
import 'vue-good-table/dist/vue-good-table.css'
import 'leaflet/dist/leaflet.css';
// Fix marker issue with Leaflet
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

Vue.config.productionTip = false;

// add plugins
Vue.use(SuiVue);
Vue.use(VueGoodTablePlugin);


new Vue({
  router,
  provide: {
    // Needed due to how semantic-ui-vue search bar works
    sui: {
      api: {
        base: process.env.VUE_APP_DJANGO_URL,
        api: {
          "search category": "/api/v1/autocomplete?startswith_str={value}"
        },
        onResponse(response) {
          return response.results;
        }
      }
    }
  },
  render: h => h(App)
}).$mount("#app");
