import Vue from "vue";
import App from "./App.vue";
import SuiVue from "semantic-ui-vue";
import router from "./router";
import VueGoodTablePlugin from 'vue-good-table';

// import the styles
import "semantic-ui-css/semantic.min.css";
import 'vue-good-table/dist/vue-good-table.css'

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
