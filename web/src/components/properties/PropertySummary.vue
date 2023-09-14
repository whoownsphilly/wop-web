<script setup lang="ts">
import {getPropertyBasicsPageInfo, getPropertyLatestOwnerDetailsInfo} from "../../services/apiFetcher";
import {Property} from "../../models/property.model";
import {onMounted, ref} from "vue";

const props  = defineProps({
  id: String
})
const property = ref(new Property())
const owner = ref({})
const link = ref()
const violationDate = ref(new Date(2006, 6, 1))

onMounted(async () => {
  const result= await getPropertyBasicsPageInfo(props.id, violationDate.value)
  property.value = Property.toProperty(result)
  const result2 = await getPropertyLatestOwnerDetailsInfo(props.id, violationDate.value)
  link.value = result2.street_view_link
  property.value.owner = result2
});

const getLicenseInspectionsLink = (address: string) => {
  return `https://li.phila.gov/property-history/search?address=${address}`;
}
</script>

<template>
  <section class="flex flex-wrap flex-col flex-col-reverse lg:flex-row justify-between ">
    <div class="w-full lg:w-1/2 h-100">
      <iframe v-if="link" class="h-[600px] w-full" :src="`${link}`"></iframe>
    </div>
    <div class="w-full lg:w-1/2 lg:pl-4 mb-4 lg:mb-0">
      <div class="text-xl">BUILDING: {{property.location}}</div>
      <div class="text-xl">LIKELY OWNER: {{owner.latest_owner}}</div>
      <div class="flex w-full border border-black divide-x divide-black">
        <div class="divide-y divide-black">
          <div class="bg-gray-200 px-2 text-center">Owner Status</div>
          <div class="p-2">{{property.hasActiveRentalLicense ? "Active Rental" : "Not Active Rental"}}</div>
        </div>
        <div class="grow divide-y divide-black">
          <div class="bg-gray-200 px-2">Rental License    (<a class="text-blue-500" :href=getLicenseInspectionsLink(property.location) target="_blank">Link to L&I</a>)</div>
          <div class="p-2">{{property.hasActiveRentalLicense ? "Active" : "None"}} : Expires {{ new Date(property.rentalLicenseExpiration).toLocaleString('en-us', { year:"numeric", month:"short", day:"numeric"})}}</div>
        </div>

      </div>
      <div class="flex w-full border-l border-r border-b border-emerald-800 divide-x divide-emerald-800">
        <div class="divide-y divide-black">
          <div class="bg-gray-200 px-2 text-center"><span class="hidden lg:block">Property</span> Type</div>
          <div class="p-2">{{property.categoryCodeDescription}}</div>
        </div>
        <div class="grow divide-y divide-black">
          <div class="bg-gray-200 px-2 text-center">Description</div>
          <div class="p-2">{{property.buildingCodeDescription}}</div>
        </div>
        <div class="divide-y divide-black">
          <div class="bg-gray-200 px-2 text-center"><span class="hidden lg:block">Year</span> Built</div>
          <div class="p-2">{{property.yearBuilt}}</div>
        </div>
        <div class="divide-y divide-black">
          <div class="bg-gray-200 px-2 text-center">Estimate</div>
          <div class="p-2">{{property.latestAssessmentMarketValue}}</div>
        </div>
      </div>
      <div class="mt-4 flex w-full border border-black">
        <div class="divide-y divide-black">
          <div class="bg-gray-200 px-2 text-center">Open Violations</div>
          <div class="text-2xl text-center pt-4"> {{ property.nViolationsOpen }}</div>
        </div>
        <div class="grow border-l border-black">
          <div class="bg-gray-200 text-center">Since {{new Date(violationDate.toLocaleString('en-us', { year:"numeric", month:"short", day:"numeric"}))}}</div>
          <div class="flex w-full">
            <div class="w-1/2 bg-gray-200 px-2 text-center">Closed Violations</div>
            <div class="w-1/2 bg-gray-200 px-2 text-center">Complaints to 311</div>
          </div>
          <div class="border-t border-black divide-x divide-black flex">
            <div class="w-1/2 text-center p-2 text-xl">{{ property.nViolationsClosedSince }}</div>
            <div class="w-1/2 text-center p-2 text-xl">{{ property.nComplaintsSince }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>

</style>