<template>
  <div style="font-size: 18px">
    <instructions-text />
    <sui-divider horizontal>Search</sui-divider>
    <sui-container>
      <sui-grid>
        <sui-grid-row>
          <sui-grid-column :width="4">
            <label for="limit_by">Number of total units:</label>
            <sui-form>
              <sui-form-fields grouped>
                <sui-form-field width="six">
                  <sui-input
                    radio
                    name="limit_by"
                    label="limit_by"
                    v-model="numTotalUnits"
                  />
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
                    label="Distance From Address"
                    value="address"
                    v-model="searchBy"
                  />
                  <sui-search
                    action="search properties"
                    v-if="searchBy == 'address'"
                    @select="searchByAddressSelected"
                    fluid
                    ref="searchBar"
                  >
                    <template v-slot:input="{ props, handlers }">
                      <sui-input
                        v-bind="props"
                        v-on:blur="handlers.blur"
                        v-on:input="handlers.input"
                        v-on:focus="handlers.focus"
                        v-model="searchByAddressSelectionTitle"
                        icon="search"
                        focus
                        fluid
                      />
                    </template>
                  </sui-search>
                </sui-form-field>
                <sui-form-field>
                  <sui-checkbox
                    radio
                    name="search_by"
                    label="Zip Code"
                    value="zipCode"
                    v-model="searchBy"
                  />
                </sui-form-field>
                <sui-form-field>
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
                    value=""
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
                    value=""
                    v-model="condoFilter"
                  />
                </sui-form-field>
              </sui-form-fields>
            </sui-form>
            <label for="condoFilter">Is Likely Owner Occupied</label>
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
                    value=""
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
    </sui-divider>

    <div v-if="loading === false">
      <leaflet-map-neighborhood
        :latLngs="allProperties"
        @updateBounds="updateBounds"
        @selectMarkers="selectMarkers"
        @addProperty="addToSelectedPropertyList"
        mapStyle="height: 350px; width: 100%"
        :customPropertyLists="customPropertyLists"
      />
    </div>
    <div v-else>
      <sui-dimmer active inverted>
        <sui-loader content="Loading..." />
      </sui-dimmer>
    </div>
    <sui-tab
      @change="handleTabChange"
      :menu="{ attached: false, tabular: false }"
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
      searchByAddressSelectionTitle: null,
      searchByAddressSelection: null,
      searchByZipCode: null,
      searchByAddressLatitude: null,
      searchByAddressLongitude: null,
      activeTabPane: null,
      searchBy: "mapBoundary",
      licenseFilter: "",
      condoFilter: "",
      ownerOccupiedFilter: "",
      numTotalUnits: 100,
      colorOptions: ["red", "green", "blue", "yellow", "orange", "pink"],
      /*colorOptions: [
        { text: "red", value: "red" },
        { text: "green", value: "green" },
      ],*/
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
      mapBounds: {},
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
    searchByAddressSelected(selection) {
      this.searchByAddressSelectionTitle = selection["title"];
      const selectionIndex = selection["url"];
      let selectedResult = this.$store.state.searchResults[selectionIndex];
      console.log(selectedResult);
      this.searchByAddressLatitude = selectedResult.lat;
      this.searchByAddressLongitude = selectedResult.lng;
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
    saveNewCustomPropertyList() {
      let listName = this.newCustomPropertyListName;
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
    updatePropertyList() {
      this.loading = true;
      getNeighborhoodsPageInfo(
        this.mapBounds,
        this.searchByZipCode,
        this.searchByAddressLatitude,
        this.searchByAddressLongitude,
        this.searchBy,
        this.licenseFilter,
        this.condoFilter,
        this.ownerOccupiedFilter,
        this.numTotalUnits,
        this.selectedBuildingTypes,
        this.selectedRentalBuildingTypes
      ).then(
        results => (
          (this.rawSearchResultProperties = results.searched_properties),
          (this.loading = false)
        )
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
        this.addToSelectedPropertyList(this.activeTabPane, marker)
      );
    },
    addToSelectedPropertyList(listName, property) {
      let thisProperty = this.propertyDict[property.parcelNumber];
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
