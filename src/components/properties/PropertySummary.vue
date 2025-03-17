<script setup lang="ts">
import {
  getPropertyBasicsPageInfo,
  getPropertyLatestOwnerDetailsInfo,
} from '../../services/apiFetcher'
import { Property } from '../../models/property.model'
import { onMounted, reactive, ref } from 'vue'
import LoadingMap from '../ui/LoadingMap.vue'

const props = defineProps({
  id: String,
})
const pageState = reactive({
  isMapLoading: true,
  isLoading: true,
})
const property = ref(new Property())
const owner = ref({})
const link = ref()
const violationDate = ref(new Date(2006, 6, 1))

onMounted(async () => {
  pageState.isLoading = true
  try {
    const [result, result2] = await Promise.all([
      getPropertyBasicsPageInfo(props.id, violationDate.value),
      getPropertyLatestOwnerDetailsInfo(props.id, violationDate.value),
    ])
    property.value = Property.toProperty(result)
    link.value = result2.street_view_link
    owner.value = result2
  } catch (error) {
    console.error('Error loading property data:', error)
  } finally {
    pageState.isLoading = false
  }
})

const frameLoaded = () => {
  pageState.isMapLoading = false
}
const getLicenseInspectionsLink = (address: string) => {
  return `https://li.phila.gov/property-history/search?address=${address}`
}
</script>

<template>
  <section class="flex flex-col flex-col-reverse flex-wrap justify-between lg:flex-row">
    <div v-if="pageState.isLoading" class="w-full">
      <div class="mb-4 flex justify-between rounded-sm bg-gray-200 p-4">
        <div class="w-full text-center">
          <span>Loading property details...</span>
        </div>
        <div
          class="h-5 w-5 animate-spin rounded-full border-2 border-emerald-800 border-t-transparent"
        ></div>
      </div>
    </div>
    <template v-else>
      <div class="h-100 w-full lg:w-1/2">
        <LoadingMap v-if="pageState.isMapLoading" />
        <iframe
          v-show="!pageState.isMapLoading"
          @load="frameLoaded()"
          v-if="link"
          class="h-[600px] w-full"
          :src="`${link}`"
        ></iframe>
      </div>
      <div class="mb-4 w-full lg:mb-0 lg:w-1/2 lg:pl-4">
        <div class="text-xl">BUILDING: {{ property.location }}</div>
        <div class="text-xl">LIKELY OWNER: {{ owner.latest_owner }}</div>
        <div class="flex w-full divide-x divide-black border border-black">
          <div class="divide-y divide-black">
            <div class="bg-gray-200 px-2 text-center">Owner Status</div>
            <div class="p-2">
              {{ property.hasActiveRentalLicense ? 'Active Rental' : 'Not Active Rental' }}
            </div>
          </div>
          <div class="grow divide-y divide-black">
            <div class="bg-gray-200 px-2">
              Rental License (<a
                class="text-blue-500"
                :href="getLicenseInspectionsLink(property.location)"
                target="_blank"
                >Link to L&I</a
              >)
            </div>
            <div class="p-2">
              {{ property.hasActiveRentalLicense ? 'Active' : 'None' }} : Expires
              {{
                new Date(property.rentalLicenseExpiration).toLocaleString('en-us', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric',
                })
              }}
            </div>
          </div>
        </div>
        <div
          class="flex w-full divide-x divide-emerald-800 border-b border-l border-r border-emerald-800"
        >
          <div class="divide-y divide-black">
            <div class="bg-gray-200 px-2 text-center">
              <span class="hidden whitespace-nowrap lg:block">Property Type</span>
            </div>
            <div class="p-2">{{ property.categoryCodeDescription }}</div>
          </div>
          <div class="grow divide-y divide-black">
            <div class="bg-gray-200 px-2 text-center">Description</div>
            <div class="p-2">{{ property.buildingCodeDescription }}</div>
          </div>
          <div class="divide-y divide-black">
            <div class="bg-gray-200 px-2 text-center">
              <span class="hidden whitespace-nowrap lg:block">Year Built</span>
            </div>
            <div class="p-2">{{ property.yearBuilt }}</div>
          </div>
          <div class="divide-y divide-black">
            <div class="bg-gray-200 px-2 text-center">Estimate</div>
            <div class="p-2">{{ property.latestAssessmentMarketValue }}</div>
          </div>
        </div>
        <div class="mt-4 flex w-full border border-black">
          <div class="divide-y divide-black">
            <div class="bg-gray-200 px-2 text-center">Open Violations</div>
            <div class="pt-4 text-center text-2xl">{{ property.nViolationsOpen }}</div>
          </div>
          <div class="grow border-l border-black">
            <div class="bg-gray-200 text-center">
              Since
              {{
                new Date(
                  violationDate.toLocaleString('en-us', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                  })
                )
              }}
            </div>
            <div class="flex w-full">
              <div class="w-1/2 bg-gray-200 px-2 text-center">Closed Violations</div>
              <div class="w-1/2 bg-gray-200 px-2 text-center">Complaints to 311</div>
            </div>
            <div class="flex divide-x divide-black border-t border-black">
              <div class="w-1/2 p-2 text-center text-xl">{{ property.nViolationsClosedSince }}</div>
              <div class="w-1/2 p-2 text-center text-xl">{{ property.nComplaintsSince }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped></style>
