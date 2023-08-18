<script setup lang="ts">
  import PropertyOwnerMap from "./PropertyOwnerMap.vue";
  import {getOwnerPageInfoByMailingAddress, getOwnerPageInfoByName} from "../../services/apiFetcher";
  import {reactive, ref} from "vue";
  import {CurrencyFormatter} from "../../services/utility.helper";

  const mailingAddressInfo = ref<any>({})
  const violationDate = ref<any>(new Date(2006, 6, 1))
  const properties = ref<any>(new Array<any>())
  const propertySummary = reactive({ amount: 0, complaints: 0, open: 0, closed: 0 })

  const props = defineProps({
    id: { type: String, required: true }
  })
  const [mailingResults, ownerResults] = await Promise.all([
    getOwnerPageInfoByMailingAddress(props.id, violationDate),
    getOwnerPageInfoByName(props.id, violationDate)])

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
</script>

<template>
  <section class="flex flex-col w-full">
    <div class="flex flex-col flex-col-reverse w-full lg:flex-row gap-4">
      <div class="w-full lg:w-1/2 h-[50vh]">
        <PropertyOwnerMap properties={properties()} />
      </div>
      <div class="w-full lg:w-1/2">
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
    </div>
    <div class="max-w-6xl">
      <table class="w-6xl">
        <thead>
        <tr>
          <th>color</th>
          <th>current_owner</th>
          <th>document_id</th>
          <th>lat</th>
          <th>likely_owner</th>
          <th>lng</th>
          <th>location</th>
          <th>location_unit</th>
          <th>mailing_address_1</th>
          <th>mailing_address_2</th>
          <th>mailing_care_of</th>
          <th>mailing_city_state</th>
          <th>mailing_street</th>
          <th>mailing_zip</th>
          <th>market_value</th>
          <th>complaints</th>
          <th>violations</th>
          <th>violations_closed</th>
          <th>violations_open</th>
          <th>opa_account_num</th>
          <th>opa_address</th>
          <th>opa_address_unit</th>
          <th>property_count</th>
          <th>sold_to</th>
          <th>source</th>
          <th>start_dt</th>
          <th>unit</th>
        </tr>
        </thead>

      </table>
    </div>
  </section>
</template>

<style scoped>

</style>