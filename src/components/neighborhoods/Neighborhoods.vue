<script setup lang="ts">
import NeighborhoodMap from './NeighborhoodMap.vue'
import { getNeighborhoodsPageInfo } from '../../services/apiFetcher.ts'
import { ref } from 'vue'

const buildingTypes = [
  { key: 'Multi Family', text: 'Multi Family', value: 'Multi Family', isRental: false },
  { key: 'Single Family', text: 'Single Family', value: 'Single Family', isRental: false },
  { key: 'Mixed Use', text: 'Mixed Use', value: 'Mixed Use', isRental: false },
  { key: 'Vacant Land', text: 'Vacant Land', value: 'Vacant Land', isRental: false },
  { key: 'Industrial', text: 'Industrial', value: 'Industrial', isRental: false },
  { key: 'Commercial', text: 'Commercial', value: 'Commercial', isRental: false },
  { key: 'Other', text: 'Other', value: 'Other', isRental: true },
  { key: 'Dormitories', text: 'Dormitories', value: 'Dormitories', isRental: true },
  {
    key: 'Residential Dwellings',
    text: 'Residential Dwellings',
    value: 'Residential Dwellings',
    isRental: true,
  },
  {
    key: 'Rooming House / Boarding House',
    text: 'Rooming/Boarding House',
    value: 'Rooming House / Boarding House',
    isRental: true,
  },
  { key: 'Hotel', text: 'Hotel', value: 'Hotel' },
]

const visibleInstructions = ref('')
const numUnitsPerList = ref(20)
const numLists = ref(5)
const startingAddress = ref('')
const zipCode = ref('')
const blocksFromAddress = ref(0)
const searchType = ref('mapBoundary')
const activeToggles = ref(['rental', 'no-rental', 'no-condo', 'no-owner'])
const activeBuildingTypes = ref([buildingTypes[0], buildingTypes[1], buildingTypes[8]])
const properties = ref<any>(new Array<any>())
const walkingLists = ref([])

const isActive = (key: string) => {
  return activeToggles.value.indexOf(key) > -1
}

const isActiveBuildingType = (value: string) => {
  return activeBuildingTypes.value.find((v) => v.value === value) !== undefined
}

const toggleActive = (key: string) => {
  const index = activeToggles.value.indexOf(key)
  if (index > -1) {
    activeToggles.value.splice(index, 1)
  } else {
    activeToggles.value.push(key)
  }
}

const toggleActiveBuildingType = (type: any) => {
  const index = activeBuildingTypes.value.indexOf(type)
  if (index > -1) {
    activeBuildingTypes.value.splice(index, 1)
  } else {
    activeBuildingTypes.value.push(type)
  }
}

const toggleVisibleInstructions = (type: string) => {
  visibleInstructions.value = visibleInstructions.value === type ? '' : type
}

const isSearchType = (key: string) => {
  return searchType.value === key
}

const getActiveToggleFilterValues = (filter) => {
  const isToggle = activeToggles.value.indexOf(filter) > -1
  const isNotToggle = activeToggles.value.indexOf('no-' + filter) > -1
  let result = null
  if (isToggle && !isNotToggle) {
    result = true
  }
  if (isNotToggle && !isToggle) {
    result = false
  }

  return result
}
const update = async () => {
  const selectedBuildingTypes = activeBuildingTypes.value
    .filter((t) => !t.isRental)
    .map((t) => t.value)
    .join(',')
  const selectedRentalBuildingTypes = activeBuildingTypes.value
    .filter((t) => t.isRental)
    .map((t) => t.value)
    .join(',')
  const mapBounds = {
    _northEast: {
      lat: 39.987642831840844,
      lng: -75.15343666076662,
    },
    _southWest: {
      lat: 39.93501296038254,
      lng: -75.24888038635255,
    },
  }

  const startingAddressLatitude = 0
  const startingAddressLongitude = 0
  let condoFilter = getActiveToggleFilterValues('condo')
  let licenseFilter = getActiveToggleFilterValues('rental')
  const ownerOccupiedFilter = getActiveToggleFilterValues('owner')

  const results = await getNeighborhoodsPageInfo(
    mapBounds,
    zipCode.value,
    blocksFromAddress.value,
    startingAddressLatitude,
    startingAddressLongitude,
    searchType.value,
    licenseFilter,
    condoFilter,
    ownerOccupiedFilter,
    numUnitsPerList.value,
    numLists.value,
    selectedBuildingTypes,
    selectedRentalBuildingTypes
  )

  if (results.status === 'error') {
    // this.loading = false;
    // this.errorMessage = "Error During Search";
    return
  } else {
    // this.errorMessage = "";
  }

  properties.value = results.searched_properties
  walkingLists.value = results.walk_lists
  console.log(walkingLists.value)
  Object.keys(results.walk_lists).forEach((walkListName) => {
    console.log(walkListName)
    // this.saveNewCustomPropertyList(walkListName);
    // results.walk_lists[walkListName].forEach(thisProperty => {
    //     this.addToSelectedPropertyList(
    //         walkListName,
    //         thisProperty.parcel_number
    //     );
    // });
  })
}
</script>

<template>
  <main class="flex flex-col justify-between gap-1">
    <section class="flex w-full justify-between gap-2 px-4 py-2">
      <div class="flex h-[150px] w-1/4 flex-col gap-1 overflow-auto">
        <h3 class="text-xl font-medium">Instructions</h3>
        <h4
          class="cursor-pointer p-1 text-sm hover:bg-neutral-200 hover:text-black"
          :class="{ 'bg-neutral-500 text-white': visibleInstructions === 'searching' }"
          @click="toggleVisibleInstructions('searching')"
        >
          Searching Properties
        </h4>
        <div v-if="visibleInstructions === 'searching'">
          <div class="pl-1 text-sm">
            Select a geographic area to find the 100 properties with the most violations in that
            area. These are properties that have an active rental license and violations are only
            counted if they occurred after 2018-01-01.
            <br /><br />
            Click "Search By: Zip Code" to enter a zip code as the geographic area of focus. Click
            "Search By: Map Boundary" to select your own geographic area of choice. You can do this
            either by zooming in on the map, or by clicking one of the shapes on the map legend and
            drawing a custom geographic area.
            <br /><br />
            Once you have selected a geographic area, click "Update Map", which will update the
            markers on the map to represent the 100 properties with the most violations within that
            area. The list below the map will also populate with this list.
          </div>
        </div>
        <h4
          class="cursor-pointer p-1 text-sm hover:bg-neutral-200"
          :class="{ 'bg-neutral-500 text-white': visibleInstructions === 'generating' }"
          @click="toggleVisibleInstructions('generating')"
        >
          Generating Lists
        </h4>
        <div v-if="visibleInstructions === 'generating'">
          <div class="p-1 text-sm">
            To generate custom lists, you first have to use the "+ Add List" tab to create a new
            list. Currently, each new list automatically gets assigned a different color. The system
            can reliably handle about 5 lists at a time, but this could be increased in the future.
            After creating a list, you can click on a property marker in the map, it's address will
            pop up along with a drop-down menu with the populated list names, and a button that says
            'Add to List'. By clicking on the address, it will then add that property to your own
            personal list, which can be subsequently downloaded.
            <br /><br />
            You can also bulk add properties to the list by going to that list's tab, using the
            selector tool on the map legend, drawing a shape on the map, and then clicking the 'Add
            map bounds to list' button.
          </div>
        </div>
        <h4
          class="cursor-pointer p-1 text-sm hover:bg-neutral-200"
          :class="{ 'bg-neutral-500 text-white': visibleInstructions === 'sharing' }"
          @click="toggleVisibleInstructions('sharing')"
        >
          Sharing Lists
        </h4>
        <div v-if="visibleInstructions === 'sharing'">
          <div class="p-1 text-sm">
            After creating a list, you can share out 2 different types of links. There is a 'Link to
            read-only version of this List' which will link people directly to what is inside the
            Tab (a copy of the list and a map of just those selected properties). There is also a
            'Link to walking directions' which will open up all of the selected properties in an
            external Google Maps page.
            <br /><br />
            If you are working on a list and are not completed with it, you can copy the URL (which
            changes whenever a property is added) and that URL should return you to the same list
            that you were working on.
          </div>
        </div>
      </div>
      <div class="flex w-1/2 flex-col gap-1">
        <h3 class="text-xl font-medium">Building Type</h3>
        <div class="flex flex-wrap">
          <button
            v-for="type in buildingTypes"
            v-bind:key="type.value"
            class="toggle-button w-1/3"
            :class="{ active: isActiveBuildingType(type.value) }"
            @click="toggleActiveBuildingType(type)"
          >
            {{ type.text }}
          </button>
        </div>
      </div>
      <div class="flex w-1/4 flex-col justify-start gap-2">
        <h3 class="text-xl font-medium">Features</h3>
        <div class="flex flex-wrap">
          <button
            class="toggle-button w-1/2"
            :class="{ active: isActive('rental') }"
            @click="toggleActive('rental')"
          >
            Rental License
          </button>
          <button
            class="toggle-button w-1/2"
            :class="{ active: isActive('no-rental') }"
            @click="toggleActive('no-rental')"
          >
            No Rental License
          </button>
          <button
            class="toggle-button w-1/2"
            :class="{ active: isActive('condo') }"
            @click="toggleActive('condo')"
          >
            In Condo
          </button>
          <button
            class="toggle-button w-1/2"
            :class="{ active: isActive('no-condo') }"
            @click="toggleActive('no-condo')"
          >
            Not in Condo
          </button>
          <button
            class="toggle-button w-1/2"
            :class="{ active: isActive('owner') }"
            @click="toggleActive('owner')"
          >
            Owner Occupied
          </button>
          <button
            class="toggle-button w-1/2"
            :class="{ active: isActive('no-owner') }"
            @click="toggleActive('no-owner')"
          >
            Not Owner Occupied
          </button>
        </div>
      </div>
    </section>
    <section class="flex items-center border-b border-t px-4">
      <div class="whitespace-nowrap px-4 py-2 font-medium uppercase">Search By</div>
      <div class="flex w-full justify-start border-l py-2">
        <select
          class="mx-2 block w-1/3 w-[200px] rounded-md border border-gray-200 px-4 py-2 pr-9 text-sm"
          v-model="searchType"
        >
          <option selected value="mapBoundary">Map</option>
          <option value="address">Address</option>
          <option value="zipCode">Zip Code</option>
        </select>
        <div v-if="isSearchType('address')" class="flex w-full">
          <div class="mr-2 flex grow items-center gap-2">
            <input
              type="text"
              class="w-1/3 grow rounded-sm border p-2"
              placeholder="Starting Address"
              v-model="startingAddress"
            />
          </div>
          <div class="flex flex-row items-center justify-between gap-2">
            <input
              type="text"
              class="w-[50px] rounded-sm border px-2 py-2 text-right"
              v-model="blocksFromAddress"
            />
            <div class="whitespace-nowrap text-sm text-gray-400">Blocks from Address</div>
          </div>
        </div>
        <div v-if="isSearchType('zipCode')">
          <div class="flex items-center gap-2">
            <input
              type="text"
              class="w-full rounded-sm border p-2"
              placeholder="Zip Code"
              v-model="zipCode"
            />
          </div>
        </div>
      </div>
    </section>
    <section class="flex h-[600px] w-full gap-4 px-4">
      <div>
        <button
          class="my-2 mr-4 w-full rounded-sm bg-emerald-700 px-4 py-2 text-white"
          @click="update"
        >
          Update Map
        </button>
        <div class="flex items-center justify-between gap-2">
          <div class="text-sm">Units per list</div>
          <input
            type="text"
            class="w-1/3 rounded-sm border px-2 py-1 text-right"
            v-model="numUnitsPerList"
          />
        </div>
        <div class="flex items-center justify-between gap-2">
          <div class="text-sm">Number of lists</div>
          <input
            type="text"
            class="w-1/3 rounded-sm border px-2 py-1 text-right"
            v-model="numLists"
          />
        </div>

        <h3 class="text-xl font-medium">Searched Properties</h3>
        <div v-for="walkingList in walkingLists" v-bind:key="walkingList.location">
          <div>{{ walkingList.location }} {{ walkingLists.length }}</div>
        </div>
        <div v-if="walkingLists.length === 0">
          <div class="bg-gray-100 p-4 text-center">No Results</div>
        </div>
      </div>
      <div class="w-3/4">
        <NeighborhoodMap :properties="properties" />
      </div>
    </section>
  </main>
</template>

<style scoped>
.toggle-button {
  @apply border bg-neutral-100 px-4 py-1 text-xs text-neutral-400;
}

.search-toggle-button {
  @apply border bg-neutral-100 px-6 py-2 text-neutral-400;
}

.active {
  @apply bg-neutral-500 text-white;
}
</style>
