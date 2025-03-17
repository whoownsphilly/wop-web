<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const domain = import.meta.env.PUBLIC_API_DOMAIN || 'https://api.whoownsphilly.org/'

const filteredItems = ref([])
const isLoading = ref(false)
const searchInput = ref('')
let debounceTimeout: number | null = null

const filterItems = async (event) => {
  const inputValue = event.target.value
  searchInput.value = inputValue

  // Clear any existing timeout
  if (debounceTimeout) {
    clearTimeout(debounceTimeout)
  }

  // Don't search if input is too short
  if (!inputValue || inputValue.length <= 3) {
    filteredItems.value = []
    return
  }

  // Set loading state
  isLoading.value = true

  // Debounce the API call by 300ms
  debounceTimeout = setTimeout(async () => {
    try {
      const endpoint = `${domain}api/v1/autocomplete?startswith_str=${inputValue.toLowerCase()}`
      const result = await axios.get(endpoint)
      // Only update results if the input hasn't changed during the request
      if (searchInput.value === inputValue) {
        filteredItems.value = result.data.results
      }
    } catch (error) {
      console.error('Error fetching autocomplete results:', error)
      filteredItems.value = []
    } finally {
      // Only clear loading state if this is still the latest request
      if (searchInput.value === inputValue) {
        isLoading.value = false
      }
    }
  }, 300)
}
</script>

<template>
  <section class="relative w-full">
    <div class="relative">
      <input
        class="w-full rounded-full border px-8 py-4 text-xl hover:shadow-md focus:shadow-md focus:outline-none"
        type="text"
        @input="filterItems"
        placeholder="Search address owner..."
      />
      <div v-if="isLoading" class="absolute right-4 top-1/2 -translate-y-1/2 transform">
        <div
          class="h-5 w-5 animate-spin rounded-full border-2 border-emerald-800 border-t-transparent"
        ></div>
      </div>
    </div>
    <div v-if="filteredItems.length > 0" class="absolute z-10 w-full">
      <ul class="mt-1 w-full divide-y rounded-sm border bg-white shadow-md">
        <li
          class="p-2 hover:cursor-pointer hover:bg-gray-50 hover:text-emerald-800"
          v-for="item in filteredItems"
          v-bind:key="item.computed_location"
        >
          <a :href="`/properties/${item['opa_account_num']}/summary`">{{
            item.computed_location
          }}</a>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped></style>
