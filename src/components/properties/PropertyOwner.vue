<script setup lang="ts">
import PropertyOwnerMap from './PropertyOwnerMap.vue'
import { getOwnerPageInfoByMailingAddress, getOwnerPageInfoByName } from '../../services/apiFetcher'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { CurrencyFormatter } from '../../services/utility.helper'
import LoadingMap from '../ui/LoadingMap.vue'
import { IconLoader5Line } from '@iconify-prerendered/vue-ri'

const mailingAddressInfo = ref<any>({})
const ownerInfo = ref({})
const violationDate = ref<any>(new Date(2006, 6, 1))
const properties = ref<any>(new Array<any>())
const propertySummary = reactive({ amount: 0, complaints: 0, open: 0, closed: 0 })

const props = defineProps({
  id: { type: String, required: true },
})

const pageState = reactive({
  isLoading: true,
  loadingPercent: 0,
  activeListTab: 'owner',
  activeListType: 'timeline',
})

const filteredList = computed(() => {
  const list = pageState.activeListTab === 'owner' ? ownerInfo.value : mailingAddressInfo.value
  return list[pageState.activeListType]
})

const getPropertyLink = (id: number) => {
  return `/properties/${id}/summary`
}

const loadData = async (propertyId: string) => {
  pageState.isLoading = true

  // TODO add date parameter
  const [mailingResults, ownerResults] = await Promise.all([
    getOwnerPageInfoByMailingAddress(propertyId),
    getOwnerPageInfoByName(propertyId),
  ])

  mailingAddressInfo.value = {
    mailingAddress: mailingResults['metadata']['mailing_address'],
    names: mailingResults['results']['alias_names'],
    mailingCareOfNames: mailingResults['results']['mailing_care_of_names'],
    timeline: mailingResults['results']['timeline'],
    violations: mailingResults['results']['violations'],
    complaints: mailingResults['results']['complaints'],
    ownerPropertyCountsByName: mailingResults['display_inputs']['owner_property_counts_by_name'],
  }

  ownerInfo.value = {
    timeline: ownerResults['results']['timeline'],
    violations: ownerResults['results']['violations'],
    complaints: ownerResults['results']['complaints'],
    names: ownerResults['results']['alias_names'],
    ownerPropertyCountsByName: ownerResults['display_inputs']['owner_property_counts_by_name'],
  }

  const allProperties = ownerInfo.value.timeline.concat(mailingAddressInfo.value.timeline)

  let allUniqueCurrentProperties = []
  let allUniquePropertyParcelNumbers = []
  allProperties.forEach((property) => {
    if (!allUniquePropertyParcelNumbers.includes(property.opa_account_num)) {
      allUniquePropertyParcelNumbers.push(property.opa_account_num)
      propertySummary.open += property.n_violations_open
      propertySummary.closed += property.n_violations_closed
      propertySummary.complaints += property.n_complaints
      propertySummary.amount += property.market_value
      if (property.current_owner === true) {
        allUniqueCurrentProperties.push(property)
      }
    }
  })
  properties.value = allUniqueCurrentProperties
  pageState.isLoading = false
}
onMounted(async () => {
  // TODO return these first but run in parallel. RXJS?
  await loadData(props.id)
})

watch(
  () => props.id,
  async (value) => {
    await loadData(value)
  }
)
</script>

<template>
  <section class="flex w-full flex-col">
    <div v-if="pageState.isLoading" class="mb-4 flex justify-between rounded-sm bg-gray-200 p-4">
      <div class="w-full text-center">
        <span>Loading could take up to 30 seconds</span>
      </div>
      <icon-loader5-line class="animate-spin text-2xl text-gray-500" />
    </div>
    <div class="flex w-full flex-col flex-col-reverse gap-4 lg:flex-row">
      <div class="h-[80vh] w-full lg:w-1/2">
        <LoadingMap v-if="pageState.isLoading" />
        <PropertyOwnerMap :properties="properties" v-if="!pageState.isLoading" />
      </div>
      <div class="flex w-full flex-col lg:w-1/2">
        <div>
          <div>
            <div class="font-bold">Mailing Address</div>
            <span class="text-sm lg:text-xl"> {{ mailingAddressInfo.mailingAddress }}</span>
          </div>
          <div
            v-if="mailingAddressInfo.mailingAddressBasedMailingCareOfNames"
            class="text-sm lg:text-base"
          >
            <div class="border-t pt-2">Mailing Care Of</div>
            <span> {{ mailingAddressInfo.mailingAddressBasedMailingCareOfNames.join(', ') }}</span>
          </div>
          <div class="flex w-full flex-col divide-emerald-800 border border-black">
            <div class="bg-neutral-300 text-center">Properties currently associated with owner</div>
            <div class="flex w-full">
              <div class="w-1/2 bg-neutral-300 px-2 text-center">Properties</div>
              <div class="w-1/2 bg-neutral-300 px-2 text-center">Total Value</div>
            </div>
            <div class="flex divide-x divide-black border-t border-black">
              <div class="w-1/2 p-2 text-center text-xl">{{ properties.length }}</div>
              <div class="w-1/2 p-2 text-center text-xl">
                {{ CurrencyFormatter.USDollar.format(propertySummary.amount) }}
              </div>
            </div>
          </div>
          <div class="mt-4 flex w-full border border-black">
            <div class="divide-y divide-black">
              <div class="bg-neutral-300 px-2 text-center">Open Violations</div>
              <div class="pt-4 text-center text-2xl">{{ propertySummary.open }}</div>
            </div>
            <div class="grow border-l border-black">
              <div class="bg-neutral-300 text-center">
                Since
                {{
                  new Date(violationDate).toLocaleString('en-us', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                  })
                }}
              </div>
              <div class="flex w-full">
                <div class="w-1/2 bg-neutral-300 px-2 text-center">Closed Violations</div>
                <div class="w-1/2 bg-neutral-300 px-2 text-center">Complaints</div>
              </div>
              <div class="flex divide-x divide-black border-t border-black">
                <div class="w-1/2 p-2 text-center text-xl">{{ propertySummary.closed }}</div>
                <div class="w-1/2 p-2 text-center text-xl">{{ propertySummary.complaints }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex grow flex-col">
          <h3 class="mb-2 mt-4 flex w-full justify-between font-bold">
            Property Violations<span class="font-normal"
              >Record Count: {{ filteredList?.length }}</span
            >
          </h3>
          <div class="flex w-full">
            <button
              class="nav-button w-full"
              :class="{ active: pageState.activeListTab === 'owner' }"
              @click="pageState.activeListTab = 'owner'"
            >
              Owner
            </button>
            <button
              class="nav-button w-full"
              :class="{ active: pageState.activeListTab === 'mailing' }"
              @click="pageState.activeListTab = 'mailing'"
            >
              Mailing Address
            </button>
          </div>
          <div class="mt-1 flex w-full">
            <button
              class="nav-button w-full"
              :class="{ active: pageState.activeListType === 'timeline' }"
              @click="pageState.activeListType = 'timeline'"
            >
              Properties
            </button>
            <button
              class="nav-button w-full"
              :class="{ active: pageState.activeListType === 'violations' }"
              @click="pageState.activeListType = 'violations'"
            >
              Violations
            </button>
            <button
              class="nav-button w-full"
              :class="{ active: pageState.activeListType === 'complaints' }"
              @click="pageState.activeListType = 'complaints'"
            >
              311 Complaints
            </button>
          </div>
          <!-- TODO
          Show different columns for each type
          properties:  likely_owner, location, unit, n_days_owned, n_complaints, n_violations, n_violations_open, opa_account_num
          violations:  likely_owner, location, unit, opa_account_num, violationcodetitle, violationdate, violationnumber, violationresolutioncode, violationstatus
          complaints: likely_owner, location, unit, complaint_date, complaint_number, complaint (empty right now), opa_account_num
          -->
          <div class="h-[50vh]] grow overflow-auto">
            <div
              class="mt-2 flex items-center border pr-2"
              v-if="pageState.activeListTab === 'mailing'"
            >
              <span class="mr-2 bg-gray-100 px-2 py-1">NAMES</span>
              {{ mailingAddressInfo.names.join('; ') }}
            </div>
            <table class="w-full text-xs sm:text-sm" v-if="pageState.activeListType === 'timeline'">
              <thead>
                <tr>
                  <th colspan="4"></th>
                  <th colspan="2" class="text-center">Violations</th>
                  <th></th>
                </tr>
                <tr>
                  <th v-if="pageState.activeListTab === 'owner'">Owner</th>
                  <th>Location</th>
                  <th>Days <span class="hidden sm:block">Owned</span></th>
                  <th>Complaints</th>
                  <th>Total</th>
                  <th>Open</th>
                  <th>OPA <span class="hidden sm:block">Number</span></th>
                </tr>
              </thead>
              <tbody>
                <tr
                  class="hover:bg-gray-100"
                  v-for="(item, index) in filteredList"
                  v-bind:key="index"
                >
                  <td v-if="pageState.activeListTab === 'owner'">{{ item.likely_owner }}</td>
                  <td class="whitespace-nowrap">{{ item.location }} {{ item?.unit }}</td>
                  <td class="text-right">{{ item.n_days_owned }}</td>
                  <td class="text-right">{{ item.n_complaints }}</td>
                  <td class="text-right">{{ item.n_violations }}</td>
                  <td class="text-right">{{ item.n_violations_open }}</td>
                  <td class="text-right">
                    <a :href="getPropertyLink(item.opa_account_num)">{{ item.opa_account_num }}</a>
                  </td>
                </tr>
              </tbody>
            </table>
            <table
              class="w-full text-xs sm:text-sm"
              v-if="pageState.activeListType === 'violations'"
            >
              <thead>
                <tr>
                  <th v-if="pageState.activeListTab === 'owner'">Owner</th>
                  <th>Location</th>
                  <th>Title</th>
                  <th>Date</th>
                  <th>Number</th>
                  <th>Resolution</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody class="whitespace-nowrap text-xs">
                <tr
                  class="hover:bg-gray-100"
                  v-for="(item, index) in filteredList"
                  v-bind:key="index"
                >
                  <td v-if="pageState.activeListTab === 'owner'">{{ item.likely_owner }}</td>
                  <td>{{ item.location }} {{ item?.unit }}</td>
                  <td>{{ item.violationcodetitle }}</td>
                  <td>{{ item.violationdate }}</td>
                  <td>{{ item.violationnumber }}</td>
                  <td>{{ item.violationstatus }}</td>
                  <td>{{ item.violationresolutioncode }}</td>
                </tr>
              </tbody>
            </table>
            <table
              class="w-full text-xs sm:text-sm"
              v-if="pageState.activeListType === 'complaints'"
            >
              <thead>
                <tr>
                  <th v-if="pageState.activeListTab === 'owner'">Owner</th>
                  <th>Location</th>
                  <th>Date</th>
                  <th>Number</th>
                  <th>Complaint</th>
                </tr>
              </thead>
              <tbody class="whitespace-nowrap">
                <tr
                  class="hover:bg-gray-100"
                  v-for="(item, index) in filteredList"
                  v-bind:key="index"
                >
                  <td v-if="pageState.activeListTab === 'owner'">{{ item.likely_owner }}</td>
                  <td>{{ item.location }} {{ item?.unit }}</td>
                  <td>{{ item.complaintdate }}</td>
                  <td>{{ item.complaintnumber }}</td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
table tbody tr td {
  @apply pr-1;
}
.nav-button {
  @apply rounded-sm border border-white bg-gray-100 px-6 py-2 text-black;
}

.nav-button:hover {
  @apply bg-neutral-400 text-white;
}

.active {
  @apply bg-neutral-500 text-white;
}
</style>
