<template>
  <div style="font-size: 18px">
    <instructions-text />
    <sui-divider horizontal>Search</sui-divider>
    <sui-container>
      <sui-grid>
        <sui-grid-row>
          <sui-grid-column :width="4">
            <sui-form>
              <sui-form-fields grouped>
                <sui-form-field>
                  <label for="limit_by">Number of units per list:</label>
                  <sui-input
                    name="limit_by"
                    label="limit_by"
                    v-model="numUnitsPerList"
                  />
                  <label for="number_of_lists">Number of lists:</label>
                  <sui-input
                    radio
                    name="number_of_lists"
                    label="number_of_lists"
                    v-model="numLists"
                  />
                </sui-form-field>
                <sui-form-field>
                  <label for="searchBar">Starting Address</label>
                  <sui-search
                    action="search properties"
                    @select="startingAddressSelected"
                    fluid
                    ref="searchBar"
                  >
                    <template v-slot:input="{ props, handlers }">
                      <sui-input
                        v-bind="props"
                        v-on:blur="handlers.blur"
                        v-on:input="handlers.input"
                        v-on:focus="handlers.focus"
                        v-model="startingAddressSelectionTitle"
                        icon="search"
                        focus
                        fluid
                      />
                    </template>
                  </sui-search>
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
            <label for="search_by">Search By:</label>
            <sui-form>
              <sui-form-fields grouped>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="search_by"
                    label="Map Boundary"
                    value="mapBoundary"
                    v-model="searchBy"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="search_by"
                    label="Number of blocks from address"
                    value="address"
                    v-model="searchBy"
                  />
                  <sui-input
                    v-model="searchByStartingAddressDistance"
                    v-if="searchBy == 'address'"
                    placeholder="Enter number of blocks away here..."
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="search_by"
                    label="Zip Code"
                    value="zipCode"
                    v-model="searchBy"
                  />
                  <sui-input
                    v-model="searchByZipCode"
                    v-if="searchBy == 'zipCode'"
                    placeholder="Enter zip code here..."
                  />
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
          </sui-grid-column>
          <sui-grid-column :width="4">
            Filter By: <br />Building Type
            <sui-dropdown
              direction="upward"
              multiple
              fluid
              :options="buildingTypes"
              placeholder="Building Type"
              search
              selection
              v-model="selectedBuildingTypes"
            />
            Filter By: <br />Rental Building Type
            <sui-dropdown
              direction="upward"
              multiple
              fluid
              :options="rentalBuildingTypes"
              placeholder="Rental Building Type"
              search
              selection
              v-model="selectedRentalBuildingTypes"
            />
          </sui-grid-column>
          <sui-grid-column :width="6">
            <label for="licenseFilter">Rental License</label>
            <sui-form>
              <sui-form-fields grouped>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="licenseFilter"
                    label="with license"
                    value="true"
                    v-model="licenseFilter"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="licenseFilter"
                    label="without license"
                    value="false"
                    v-model="licenseFilter"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="licenseFilter"
                    label="both with and without license"
                    value="null"
                    v-model="licenseFilter"
                  />
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
            <label for="condoFilter">Is in a Condo</label>
            <sui-form>
              <sui-form-fields grouped>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="condoFilter"
                    label="is in a condo building"
                    value="true"
                    v-model="condoFilter"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="condoFilter"
                    label="is not in a condo building"
                    value="false"
                    v-model="condoFilter"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="condoFilter"
                    label="both in and not in condo buildings"
                    value="null"
                    v-model="condoFilter"
                  />
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
            <label for="ownerOccupiedFilterFilter"
              >Is Likely Owner Occupied</label
            >
            <sui-form>
              <sui-form-fields grouped>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="ownerOccupiedFilter"
                    label="license says owner-occupied or has homestead exemption"
                    value="true"
                    v-model="ownerOccupiedFilter"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="ownerOccupiedFilter"
                    label="license doesn't say owner occupied or doesn't have a homestead exemption"
                    value="false"
                    v-model="ownerOccupiedFilter"
                  />
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="ownerOccupiedFilter"
                    label="license can say either, property may or may not have exemption"
                    value="null"
                    v-model="ownerOccupiedFilter"
                  />
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
    </sui-container>
    <sui-divider horizontal>
      <sui-button v-on:click="updatePropertyList">Update Map</sui-button>
      <sui-button v-on:click="clearPropertyList">Clear</sui-button>
    </sui-divider>
    <div v-if="errorMessage" class="ui negative message">
      {{ errorMessage }}
    </div>

    <div v-if="loading === false">
      <leaflet-map-neighborhood
        :latLngs="allProperties"
        :zoom="mapZoom"
        :center="mapCenter"
        @updateBounds="updateBounds"
        @selectMarkers="selectMarkers"
        @addProperty="addToSelectedPropertyList"
        mapStyle="height: 800px; width: 100%"
        :customPropertyLists="customPropertyLists"
      />
    </div>
    <div v-else>
      <sui-dimmer active inverted>
        <sui-loader content="Loading..." />
      </sui-dimmer>
    </div>
    <sui-button v-on:click="downloadExcel">Download</sui-button>
    <sui-tab
      @change="handleTabChange"
      :menu="{ attached: false, tabular: false, vertical: true }"
      :key="lastUpdated"
    >
      <sui-tab-pane title="+ (Add List)" :attached="false">
        <h2>Add a new list</h2>
        <sui-input
          placeholder="Put name here..."
          v-model="newCustomPropertyListName"
        />
        <!--<sui-dropdown
          placeholder="Color"
          selection
          :options="colorOptions"
          v-model="newCustomPropertyListColor"
        />-->
        <sui-button v-on:click="saveNewCustomPropertyList">Save</sui-button>
      </sui-tab-pane>
      <sui-tab-pane title="Searched Properties" :attached="false">
        <h2>Properties meeting search criteria</h2>
        <data-table :rows="allProperties" title="Properties" />
      </sui-tab-pane>

      <sui-tab-pane
        v-for="(thisList, name) in customPropertyLists"
        :key="name"
        :label="getPropertyListCountAndColor(name)"
        :title="name"
        :attached="false"
      >
        <sui-button v-on:click="addSelectionToSelectedPropertyList"
          >Add map bounds to list</sui-button
        >
        <property-list :name="name" :propertyList="thisList" />
      </sui-tab-pane>
    </sui-tab>
  </div>
</template>
<script>
import LeafletMapNeighborhood from "@/components/ui/LeafletMapNeighborhood";
import PropertyList from "@/components/page/neighborhoods/PropertyList";
import InstructionsText from "@/components/page/neighborhoods/InstructionsText";
import * as XLSX from "xlsx/xlsx.mjs";
import DataTable from "@/components/ui/DataTable";
import {
  getNeighborhoodsPageInfo,
  getNeighborhoodsPageFromParcelNumbers
} from "@/api/pages";

export default {
  name: "NeighborhoodView",
  components: {
    LeafletMapNeighborhood,
    DataTable,
    PropertyList,
    InstructionsText
  },
  data() {
    return {
      lastUpdated: null, // Needed to refresh the tab panes on clear
      startingAddressSelectionTitle: null,
      startingAddressSelection: null,
      startingAddressLatitude: null,
      startingAddressLongitude: null,
      activeTabPane: null,
      errorMessage: "",
      searchBy: "mapBoundary",
      searchByZipCode: null,
      searchByStartingAddressDistance: null,
      licenseFilter: "null",
      condoFilter: "false",
      ownerOccupiedFilter: "false",
      numUnitsPerList: 50,
      numLists: 10,
      mapZoom: 6,
      mapBounds: {},
      mapCenter: null,
      colorOptions: [
        "red",
        "green",
        "blue",
        "cyan",
        "magenta",
        "yellow",
        "orange",
        "pink",
        "purple",
        "brown",
        "lime",
        "maroon",
        "olive",
        "teal",
        "silver",
        "sky blue",
        "lavender",
        "peach",
        "periwinkle",
        "powder blue",
        "rosy brown",
        "seafoam green",
        "salmon",
        "tan",
        "turquoise"
      ],
      buildingTypes: [
        { key: "Multi Family", text: "Multi Family", value: "Multi Family" },
        { key: "Single Family", text: "Single Family", value: "Single Family" },
        { key: "Mixed Use", text: "Mixed Use", value: "Mixed Use" },
        { key: "Vacant Land", text: "Vacant Land", value: "Vacant Land" },
        { key: "Industrial", text: "Industrial", value: "Industrial" },
        { key: "Commercial", text: "Commercial", value: "Commercial" }
      ],
      rentalBuildingTypes: [
        { key: "Other", text: "Other", value: "Other" },
        { key: "Dormitories", text: "Dormitories", value: "Dormitories" },
        {
          key: "Residential Dwellings",
          text: "Residential Dwellings",
          value: "Residential Dwellings"
        },
        {
          key: "Rooming House / Boarding House",
          text: "Rooming House / Boarding House",
          value: "Rooming House / Boarding House"
        },
        { key: "Hotel", text: "Hotel", value: "Hotel" }
      ],
      selectedBuildingTypes: ["Multi Family", "Single Family"],
      selectedRentalBuildingTypes: ["Residential Dwellings"],
      selectedMarkers: [],
      newCustomPropertyListName: "",
      newCustomPropertyListColor: "red",
      customPropertyLists: {},
      customPropertyListColors: {},
      rows: [],
      columns: [],
      rawSearchResultProperties: [],
      loading: false
    };
  },
  computed: {
    searchResultProperties() {
      for (var i = 0; i < this.rawSearchResultProperties.length; i++) {
        let thisProp = this.rawSearchResultProperties[i];
        let url = `${window.location.origin}/#/property/${thisProp.parcel_number}`;
        thisProp.link = url;
      }

      return this.rawSearchResultProperties;
    },
    propertyDict() {
      let obj = {};
      this.searchResultProperties
        .concat(this.customProperties)
        .map(function(x) {
          let parcel_number = x.parcel_number;
          obj[parcel_number] = x;
        });
      return obj;
    },
    customProperties() {
      let properties = [];
      for (const [key, list] of Object.entries(this.customPropertyLists)) {
        properties.push(
          list.map(v => ({
            ...v,
            color: this.customPropertyListColors[key]
          }))
        );
      }
      return properties.flat();
    },
    allProperties() {
      let properties = this.customProperties.slice();
      let selectedParcelNumbers = properties.map(x => x.parcel_number);

      for (var i = 0; i < this.searchResultProperties.length; i++) {
        let thisProperty = this.searchResultProperties[i];
        if (!selectedParcelNumbers.includes(thisProperty.parcel_number)) {
          properties.push(thisProperty);
        }
      }
      return [...new Set(properties)];
    }
  },
  methods: {
    downloadExcel() {
      const workbook = XLSX.utils.book_new();
      /* make first worksheet */
      const firstSheetRows = Object.keys(this.customPropertyLists).map(key => {
        return {
          List: key,
          Name1: "",
          "(1) can 1:1? y/n, how many?": "",
          Name2: "",
          "(2) can 1:1? y/n, how many?": ""
        };
      });
      let worksheet = XLSX.utils.json_to_sheet(firstSheetRows);
      const maxValues = firstSheetRows.reduce((acc, obj) => {
        Object.keys(obj).forEach(key => {
          const valueLength = obj[key].toString().length + 3;
          const keyLength = key.toString().length + 3;
          acc[key] = Math.max(acc[key] || 0, valueLength, keyLength);
        });
        return acc;
      }, {});

      let maxWidths = Object.keys(maxValues).map(key => ({
        wch: maxValues[key]
      }));
      worksheet["!cols"] = maxWidths;
      XLSX.utils.book_append_sheet(workbook, worksheet, "List Assignments");

      Object.entries(this.customPropertyLists).map(function([key, rows]) {
        /* */

        const rowsForSheets = rows.map(item => {
          return {
            Address: item.location,
            Unit: item.unit,
            Owner: item.owner_most_ownership,
            Name: "",
            Phone: "",
            Email: "",
            "Notes (agitation, knows neighbors, story, commit to canvass?)\nIf vacant, not a house, do not knock, etc., note here.":
              "",
            "1:1 priority (H, M, L)": ""
          };
        });
        let worksheet = XLSX.utils.json_to_sheet(rowsForSheets);

        const maxValues = rowsForSheets.reduce((acc, obj) => {
          Object.keys(obj).forEach(key => {
            const valueLength = obj[key].toString().length + 3;
            const keyLength = key.toString().length + 3;
            acc[key] = Math.max(acc[key] || 0, valueLength, keyLength);
          });
          return acc;
        }, {});

        let maxWidths = Object.keys(maxValues).map(key => ({
          wch: maxValues[key]
        }));

        worksheet["!cols"] = maxWidths;
        XLSX.utils.book_append_sheet(workbook, worksheet, key);
      });

      /* create an XLSX file and try to save */
      const today = new Date();
      const month = today.getMonth() + 1; // Add 1 to the month since getMonth() returns a zero-based index
      const day = today.getDate();

      const formattedDate = `${month}.${day}`;
      XLSX.writeFile(workbook, `Walksheets ${formattedDate}.xlsx`, {
        compression: true
      });
    },
    startingAddressSelected(selection) {
      this.startingAddressSelectionTitle = selection["title"];
      const selectionIndex = selection["url"];
      let selectedResult = this.$store.state.searchResults[selectionIndex];
      this.startingAddressLatitude = selectedResult.lat;
      this.startingAddressLongitude = selectedResult.lng;
      this.mapCenter = [selectedResult.lat, selectedResult.lng];
      // required otherwise it zooms to the old center
      new Promise(r => setTimeout(r, 200)).then(() => (this.mapZoom = 16));
    },
    handleTabChange(e, activePane) {
      this.activeTabPane = activePane.title;
    },
    updateBounds(bounds) {
      this.mapBounds = bounds;
    },
    selectMarkers(selectedMarkers) {
      this.selectedMarkers = selectedMarkers;
    },
    saveNewCustomPropertyListOnClick() {
      this.saveNewCustomPropertyList(this.newCustomPropertyListName);
    },
    saveNewCustomPropertyList(listName) {
      if (!(listName in this.customPropertyLists)) {
        this.$set(this.customPropertyLists, listName, []);
      }
      // For now we set the color by default
      let colorIndex = Object.keys(this.customPropertyLists).length - 1;

      this.$set(
        this.customPropertyListColors,
        listName,
        this.colorOptions[colorIndex]
      );

      this.newCustomPropertyListName = "";
    },
    getPropertyListCountAndColor(name) {
      return `(${this.customPropertyLists[name].length}) (${this.customPropertyListColors[name]})`;
    },
    clearPropertyList() {
      if (Object.keys(this.$route.query).length) {
        this.$router.replace({ query: {} });
      }
      this.customPropertyLists = {};
      this.customPropertyListColors = {};
      this.rows = [];
      this.columns = [];
      this.rawSearchResultProperties = [];
      this.errorMessage = "";
      let testList = {};
      testList[new Date()] = [];
      this.lastUpdated = new Date();
    },
    updatePropertyList() {
      this.loading = true;
      getNeighborhoodsPageInfo(
        this.mapBounds,
        this.searchByZipCode,
        this.searchByStartingAddressDistance,
        this.startingAddressLatitude,
        this.startingAddressLongitude,
        this.searchBy,
        this.licenseFilter,
        this.condoFilter,
        this.ownerOccupiedFilter,
        this.numUnitsPerList,
        this.numLists,
        this.selectedBuildingTypes,
        this.selectedRentalBuildingTypes
      ).then(
        function(results) {
          if (results.status === "error") {
            this.loading = false;
            this.errorMessage = "Error During Search";
            return;
          } else {
            this.errorMessage = "";
          }
          this.rawSearchResultProperties = results.searched_properties;
          Object.keys(results.walk_lists).forEach(walkListName => {
            this.saveNewCustomPropertyList(walkListName);
            results.walk_lists[walkListName].forEach(thisProperty => {
              this.addToSelectedPropertyList(
                walkListName,
                thisProperty.parcel_number
              );
            });
          });
          this.lastUpdated = new Date();
          this.loading = false;
        }.bind(this)
      );
    },
    setColorsAndUrlToSavedPropertyLists(lists) {
      let listColors = {};
      lists.forEach(
        (value, index) => (listColors[value] = this.colorOptions[index])
      );
      return listColors;
    },
    addSelectionToSelectedPropertyList() {
      this.selectedMarkers.forEach(marker =>
        this.addToSelectedPropertyList(this.activeTabPane, marker.parcelNumber)
      );
    },
    addToSelectedPropertyList(listName, parcelNumber) {
      let thisProperty = this.propertyDict[parcelNumber];
      thisProperty["color"] = this.customPropertyListColors[listName];
      this.customPropertyLists[listName].push(thisProperty);

      this.customPropertyLists[listName] = [
        ...new Set(this.customPropertyLists[listName])
      ];

      // Convert {'list1': [{parcel: 102}, {parcel: 103}]}
      // to {'list1': [102, 103]}
      let customPropertyParcelNumberDict = {};
      Object.entries(this.customPropertyLists).map(function(entry) {
        customPropertyParcelNumberDict[entry[0]] = entry[1].map(
          x => x.parcel_number
        );
        return customPropertyParcelNumberDict;
      });
      this.$router.replace({
        name: "Neighborhoods",
        query: {
          ...customPropertyParcelNumberDict
        }
      });
    }
  },
  created() {
    this.mapBounds = {
      _northEast: { lat: 39.977523, lng: -75.136808 },
      _southWest: { lat: 39.922655, lng: -75.193699 }
    };
    // Get the property list from the parcel numbers
    this.loading = true;
    getNeighborhoodsPageFromParcelNumbers(this.$route.query).then(
      results => (
        (this.customPropertyLists = results.saved_properties),
        (this.customPropertyListColors = this.setColorsAndUrlToSavedPropertyLists(
          Object.keys(results.saved_properties)
        )),
        (this.loading = false)
      )
    );
  }
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
