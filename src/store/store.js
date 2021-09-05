import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    searchResults: {},
    selectedResult: {}
  },

  getters: {
    // Here we will create a getter
  },

  mutations: {
    // Here we will create Jenny
    updateSearchResults(state, results) {
      state.searchResults = results;
    },
    updateSelectedResult(state, result) {
      state.selectedResult = result;
    }
  },

  actions: {
    // Here we will create Larry
    updateSearchResults(context, results) {
      context.commit("updateSearchResults", results);
    },
    updateSelectedResult(context, result) {
      context.commit("updateSelectedResult", result);
    }
  }
});
