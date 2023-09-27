<script setup lang="ts">
import {ref} from "vue";
import axios from "axios";

const domain = "http://localhost:8000/"

const filteredItems = ref([]);
const filterItems = async (event) => {
  const inputValue = event.target.value
  if (event.target.value && inputValue.length > 3) {
    const endpoint = `${domain}api/v1/autocomplete?startswith_str=${inputValue.toLowerCase()}`
    const result = await axios.get(endpoint)
    filteredItems.value = result.data.results
  }
}
</script>

<template>
  <section class="w-full">
    <input class="py-4 px-8 w-full rounded-full border text-xl hover:shadow-md focus:shadow-md focus:outline-none"
           type="text"
           @input="filterItems"
           placeholder="Search address owner..."/>
    <div v-if="filteredItems.length > 0" >
      <ul class="relative mt-1 w-full border divide-y shadow-md rounded-sm">
        <li  class="p-2 hover:text-emerald-800 hover:cursor-pointer"  v-for="item in filteredItems" v-bind:key="item.computed_location">
          <a :href="`/properties/${item['opa_account_num']}/summary`">{{item.computed_location}}</a>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>

</style>