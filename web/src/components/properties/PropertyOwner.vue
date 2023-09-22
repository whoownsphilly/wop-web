<script setup lang="ts">
  import PropertyOwnerMap from "./PropertyOwnerMap.vue";
  import {getOwnerPageInfoByMailingAddress, getOwnerPageInfoByName} from "../../services/apiFetcher";
  import {onMounted, reactive, ref, watch} from "vue";
  import {CurrencyFormatter} from "../../services/utility.helper";
  import LoadingMap from "../ui/LoadingMap.vue";
  import {IconLoader5Line} from "@iconify-prerendered/vue-ri";

  const mailingAddressInfo = ref<any>({})
  const violationDate = ref<any>(new Date(2006, 6, 1))
  const properties = ref<any>(new Array<any>())
  const propertySummary = reactive({ amount: 0, complaints: 0, open: 0, closed: 0 })

  const props = defineProps({
    id: { type: String, required: true }
  })

  const pageState = reactive({
    isLoading: true,
    loadingPercent: 0,
    activeListTab: 'owner',
    activeListType: 'properties'
  })

  const loadData = async (propertyId: string) => {
    pageState.isLoading = true
    const [mailingResults, ownerResults] = await Promise.all([
      getOwnerPageInfoByMailingAddress(propertyId, violationDate.value),
      getOwnerPageInfoByName(propertyId, violationDate.value)])

    const mailingInfo = {
      mailingAddress: mailingResults["metadata"]["mailing_address"],
      mailingAddressBasedNames: mailingResults["results"]["alias_names"],
      mailingAddressBasedMailingCareOfNames:  mailingResults["results"]["mailing_care_of_names"],
      mailingAddressBasedPropertyTimelineData: mailingResults["results"]["timeline"],
      mailingAddressBasedViolations: mailingResults["results"]["violations"],
      mailingAddressBasedComplaints: mailingResults["results"]["complaints"],
      mailingAddressBasedOwnerPropertyCountsByName: mailingResults["display_inputs"]["owner_property_counts_by_name"],
    }
    mailingAddressInfo.value = mailingInfo
    const ownerInfo = {
      ownerBasedPropertyTimelineData: ownerResults["results"]["timeline"],
      ownerBasedViolations: ownerResults["results"]["violations"],
      ownerBasedComplaints: ownerResults["results"]["complaints"],
      ownerBasedNames: ownerResults["results"]["alias_names"],
      ownerBasedOwnerPropertyCountsByName: ownerResults["display_inputs"]["owner_property_counts_by_name"],
    }

    const allProperties = ownerInfo.ownerBasedPropertyTimelineData.concat(mailingInfo.mailingAddressBasedPropertyTimelineData)
    let allUniqueCurrentProperties = []
    let allUniquePropertyParcelNumbers = [];
    allProperties.forEach((property) => {
      if (
          !allUniquePropertyParcelNumbers.includes(
              property.opa_account_num
          )
      ) {
        allUniquePropertyParcelNumbers.push(property.opa_account_num);
        propertySummary.open += property.n_violations_open;
        propertySummary.closed += property.n_violations_closed;
        propertySummary.complaints += property.n_complaints;
        propertySummary.amount += property.market_value;
        if (property.current_owner === true) {
          allUniqueCurrentProperties.push(property);
        }
      }
    })
    properties.value = allUniqueCurrentProperties
    propertySummary.value = propertySummary

    pageState.isLoading = false

  }
  onMounted(async () => {
    // TODO return these first but run in parallel. RXJS?
    await loadData(props.id)
  })

  watch(() => props.id, async (value) => {
    await loadData(value)
  })

</script>

<template>
  <section class="flex flex-col w-full">
    <div v-if="pageState.isLoading" class="bg-gray-200 p-4 rounded-sm flex justify-between mb-4">
      <div class="w-full text-center">
        <span>Loading could take up to 30 seconds</span>
      </div>
      <icon-loader5-line class="animate-spin text-2xl text-gray-500"/>
    </div>
    <div class="flex flex-col flex-col-reverse w-full lg:flex-row gap-4">
      <div class="w-full lg:w-1/2 h-[80vh]">
        <LoadingMap v-if="pageState.isLoading" />
        <PropertyOwnerMap :properties=properties v-if="!pageState.isLoading" />
      </div>
      <div class="w-full lg:w-1/2">
        <div>
          <div>
            <div>Mailing Address</div>
            <span class="text-sm lg:text-xl"> {{mailingAddressInfo.mailingAddress}}</span>
          </div>
          <div v-if="mailingAddressInfo.mailingAddressBasedMailingCareOfNames" class="text-sm lg:text-base">
            <div class="border-t pt-2">Mailing Care Of</div>
            <span> {{mailingAddressInfo.mailingAddressBasedMailingCareOfNames.join(", ")}}</span>
          </div>
          <div class="flex flex-col w-full border border-black divide-emerald-800">
            <div class="bg-neutral-300 text-center">Properties currently associated with owner</div>
            <div class="flex w-full">
              <div class="w-1/2 bg-neutral-300 px-2 text-center">Properties</div>
              <div class="w-1/2 bg-neutral-300 px-2 text-center">Total Value</div>
            </div>
            <div class="border-t border-black divide-x divide-black flex">
              <div class="w-1/2 text-center p-2 text-xl">{{ properties.length }} </div>
              <div class="w-1/2 text-center p-2 text-xl">{{ CurrencyFormatter.USDollar.format(propertySummary.amount) }}</div>
            </div>
          </div>
          <div class="mt-4 flex w-full border border-black">
            <div class="divide-y divide-black">
              <div class="bg-neutral-300 px-2 text-center">Open Violations</div>
              <div class="text-2xl text-center pt-4"> {{ propertySummary.open }}</div>
            </div>
            <div class="grow border-l border-black">
              <div class="bg-neutral-300 text-center">Since {{new Date(violationDate).toLocaleString('en-us', { year:"numeric", month:"short", day:"numeric"})}}</div>
              <div class="flex w-full">
                <div class="w-1/2 bg-neutral-300 px-2 text-center">Closed Violations</div>
                <div class="w-1/2 bg-neutral-300 px-2 text-center">Complaints</div>
              </div>
              <div class="border-t border-black divide-x divide-black flex">
                <div class="w-1/2 text-center p-2 text-xl">{{ propertySummary.closed }} </div>
                <div class="w-1/2 text-center p-2 text-xl">{{ propertySummary.complaints }}</div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <h3 class="mt-4">Property Lists</h3>
          <div class="w-full flex">
            <button class="nav-button w-full" :class="{active: pageState.activeListTab === 'owner'}" @click="pageState.activeListTab = 'owner'">Owner</button>
            <button class="nav-button w-full" :class="{active: pageState.activeListTab === 'mailing'}" @click="pageState.activeListTab = 'mailing'">Mailing Address</button>
          </div>
          <div class="mt-1 w-full flex">
            <button class="nav-button w-full" :class="{active: pageState.activeListType === 'properties'}" @click="pageState.activeListType = 'properties'">Properties</button>
            <button class="nav-button w-full" :class="{active: pageState.activeListType === 'violations'}" @click="pageState.activeListType = 'violations'">Violations</button>
            <button class="nav-button w-full" :class="{active: pageState.activeListType === '311'}" @click="pageState.activeListType = '311'">311 Complaints</button>
          </div>
        </div>
      </div>
    </div>
<!--    <div class="max-w-6xl">-->
<!--      <table class="w-6xl">-->
<!--        <thead>-->
<!--        <tr>-->
<!--          <th>color</th>-->
<!--          <th>current_owner</th>-->
<!--          <th>document_id</th>-->
<!--          <th>lat</th>-->
<!--          <th>likely_owner</th>-->
<!--          <th>lng</th>-->
<!--          <th>location</th>-->
<!--          <th>location_unit</th>-->
<!--          <th>mailing_address_1</th>-->
<!--          <th>mailing_address_2</th>-->
<!--          <th>mailing_care_of</th>-->
<!--          <th>mailing_city_state</th>-->
<!--          <th>mailing_street</th>-->
<!--          <th>mailing_zip</th>-->
<!--          <th>market_value</th>-->
<!--          <th>complaints</th>-->
<!--          <th>violations</th>-->
<!--          <th>violations_closed</th>-->
<!--          <th>violations_open</th>-->
<!--          <th>opa_account_num</th>-->
<!--          <th>opa_address</th>-->
<!--          <th>opa_address_unit</th>-->
<!--          <th>property_count</th>-->
<!--          <th>sold_to</th>-->
<!--          <th>source</th>-->
<!--          <th>start_dt</th>-->
<!--          <th>unit</th>-->
<!--        </tr>-->
<!--        </thead>-->

<!--      </table>-->
<!--    </div>-->
  </section>
</template>

<style scoped>
.nav-button {
  @apply px-6 py-2 rounded-sm bg-gray-100 border border-white text-black;
}

.nav-button:hover {
  @apply bg-neutral-400 text-white
}

.active  {
  @apply bg-neutral-500 text-white
}
</style>