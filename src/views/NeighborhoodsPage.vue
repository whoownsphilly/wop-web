<template>
  <div style="font-size: 18px">
    <p>
      Select a geographic area to find the 100 properties with the most
      violations in that area. These are properties that have an active rental
      license and violations are only counted if they occurred after 2018-01-01.
    </p>
    <p>
      Click <b>"Search By: Zip Code"</b> to enter a zip code as the geographic
      area of focus. Click <b>"Search By: Map Boundary"</b> to select your own
      geographic area of choice. You can do this either by zooming in on the
      map, or by clicking one of the shapes on the map legend and drawing a
      custom geographic area.
    </p>
    <p>
      Once you have selected a geographic area, click "Update Map", which will
      update the markers on the map to represent the 100 properties with the
      most violations within that area. The list below the map will also
      populate with this list. If you click on a property marker in the map,
      it's address will pop up. By clicking on the address, it will then add
      that property to your own personal list, which can be subsequently
      downloaded.
    </p>
    <sui-grid>
      <sui-grid-row>
        <sui-grid-column :width="2">
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
                  label="Zip Code"
                  value="zipCode"
                  v-model="searchBy"
                />
              </sui-form-field>
            </sui-form-fields>
          </sui-form>
        </sui-grid-column>
        <sui-grid-column :width="4">
          <sui-input
            v-model="zipCode"
            v-if="searchBy != 'mapBoundary'"
            placeholder="Enter zip code here..."
          />
        </sui-grid-column>
        <sui-grid-column :width="6">
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
        </sui-grid-column>
      </sui-grid-row>
    </sui-grid>
    <sui-divider horizontal>
      <sui-button v-on:click="updatePropertyList">Update Map</sui-button>
    </sui-divider>

    <div v-if="loading === false">
      <leaflet-map-neighborhood
        :latLngs="allProperties"
        @updateBounds="updateBounds"
        @addProperty="addToSelectedPropertyList"
        mapStyle="height: 350px; width: 100%"
        :includeLegend="includeLegend"
        :customPropertyLists="customPropertyLists"
      />
    </div>
    <div v-else>
      <sui-dimmer active inverted>
        <sui-loader content="Loading..." />
      </sui-dimmer>
    </div>
    <sui-tab>
      <sui-tab-pane title="All Properties">
        <h2>Properties meeting search criteria</h2>
        <data-table :rows="allProperties" title="Properties" />
      </sui-tab-pane>
      <sui-tab-pane title="+ (Add List)">
        <h2>Add a new list</h2>
        <sui-input
          placeholder="Put name here..."
          v-model="newCustomPropertyListName"
        />
        <sui-dropdown
          placeholder="Color"
          selection
          :options="colorOptions"
          v-model="newCustomPropertyListColor"
        />
        <sui-button v-on:click="saveNewCustomPropertyList">Save</sui-button>
      </sui-tab-pane>

      <sui-tab-pane
        v-for="(thisList, name) in customPropertyLists"
        :key="name"
        :title="getPropertyListNameAndCount(name)"
      >
        <h2>{{ name }}</h2>
        <data-table :rows="thisList" :title="name" />
      </sui-tab-pane>
    </sui-tab>
  </div>
</template>
<script>
import LeafletMapNeighborhood from "@/components/ui/LeafletMapNeighborhood";
import DataTable from "@/components/ui/DataTable";
import { getNeighborhoodsPageInfo } from "@/api/pages";

export default {
  name: "NeighborhoodView",
  data() {
    return {
      searchBy: "mapBoundary",
      buildingTypes: [
        { key: "Multi Family", text: "Multi Family", value: "Multi Family" },
        { key: "Single Family", text: "Single Family", value: "Single Family" },
        { key: "Mixed Use", text: "Mixed Use", value: "Mixed Use" },
        { key: "Vacant Land", text: "Vacant Land", value: "Vacant Land" },
        { key: "Industrial", text: "Industrial", value: "Industrial" },
        { key: "Commercial", text: "Commercial", value: "Commercial" },
      ],
      selectedBuildingTypes: ["Multi Family", "Single Family"],
      newCustomPropertyListName: "",
      newCustomPropertyListColor: "red",
      colorOptions: [
        { text: "red", value: "red" },
        { text: "green", value: "green" },
      ],
      customPropertyLists: {},
      customPropertyListColors: {},
      includeLegend: false,
      rows: [],
      columns: [],
      rawSearchResultProperties: [],
      mapBounds: {},
      zipCode: null,
      loading: false,
    };
  },
  components: {
    LeafletMapNeighborhood,
    DataTable,
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
      this.searchResultProperties.map(function(x) {
        let parcel_number = x.parcel_number;
        obj[parcel_number] = x;
      });
      return obj;
    },
    allProperties() {
      let properties = Object.values(this.customPropertyLists).flat();
      let selectedParcelNumbers = properties.map((x) => x.parcel_number);

      for (var i = 0; i < this.searchResultProperties.length; i++) {
        let thisProperty = this.searchResultProperties[i];
        if (!selectedParcelNumbers.includes(thisProperty.parcel_number)) {
          properties.push(thisProperty);
        }
      }
      return [...new Set(properties)];
    },
  },
  methods: {
    updateBounds(bounds) {
      this.mapBounds = bounds;
    },
    saveNewCustomPropertyList() {
      let listName = this.newCustomPropertyListName;
      if (!(listName in this.customPropertyLists)) {
        this.$set(this.customPropertyLists, listName, []);
      }
      this.$set(
        this.customPropertyListColors,
        listName,
        this.newCustomPropertyListColor
      );

      this.newCustomPropertyListName = "";
    },
    getPropertyListNameAndCount(name) {
      return `${name} (${this.customPropertyLists[name].length}) (${this.customPropertyListColors[name]})`;
    },
    updatePropertyList() {
      this.loading = true;
      getNeighborhoodsPageInfo(
        this.mapBounds,
        this.zipCode,
        this.searchBy,
        this.selectedBuildingTypes
      ).then(
        (results) => (
          (this.rawSearchResultProperties = results.properties),
          (this.loading = false)
        )
      );
    },
    addToSelectedPropertyList(listName, property) {
      let thisProperty = this.propertyDict[property.parcelNumber];
      thisProperty["color"] = this.customPropertyListColors[listName];
      this.customPropertyLists[listName].push(thisProperty);
      this.customPropertyLists[listName] = [
        ...new Set(this.customPropertyLists[listName]),
      ];
    },
  },
  created() {
    this.mapBounds = {
      _northEast: { lat: null, lng: null },
      _southWest: { lat: null, lng: null },
    };
    this.updatePropertyList();
  },
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
