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
      map, or <i><b>by clicking one of the shapes on the map legend</b></i> and
      drawing a custom geographic area.
    </p>
    <p>
      Once you have selected a geographic area, click "Update Map", which will
      update the markers on the map to represent the 100 properties with the
      most violations within that area. The list below the map will also
      populate with this list.
    </p>
    <p>
      To generate custom lists, you first have to use the "+ Add List" tab to
      create a new list. Currently, each new list automatically gets assigned a
      different color. The system can reliably handle about 5 lists at a time,
      but this could be increased in the future. After creating a list, you can
      click on a property marker in the map, it's address will pop up along with
      a drop-down menu with the populated list names, and a button that says
      'Add to List'. By clicking on the address, it will then add that property
      to your own personal list, which can be subsequently downloaded.
    </p>
    <p>
      After creating a list, you can share out 2 different types of links. There
      is a 'Link to read-only version of this List' which will link people
      directly to what is inside the Tab (a copy of the list and a map of just
      those selected properties). There is also a 'Link to walking directions'
      which will open up all of the selected properties in an external Google
      Maps page.
    </p>
    <p>
      If you are working on a list and are not completed with it, you can copy
      the URL (which changes whenever a property is added) and that URL should
      return you to the same list that you were working on.
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
          >Button</sui-button
        >
        <property-list :name="name" :propertyList="thisList" />
      </sui-tab-pane>
    </sui-tab>
  </div>
</template>
<script>
import LeafletMapNeighborhood from "@/components/ui/LeafletMapNeighborhood";
import PropertyList from "@/components/page/neighborhoods/PropertyList";
import DataTable from "@/components/ui/DataTable";
import {
  getNeighborhoodsPageInfo,
  getNeighborhoodsPageFromParcelNumbers,
} from "@/api/pages";

export default {
  name: "NeighborhoodView",
  components: {
    LeafletMapNeighborhood,
    DataTable,
    PropertyList,
  },
  data() {
    return {
      activeTabPane: null,
      searchBy: "mapBoundary",
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
        { key: "Commercial", text: "Commercial", value: "Commercial" },
      ],
      selectedBuildingTypes: ["Multi Family", "Single Family"],
      selectedMarkers: [],
      newCustomPropertyListName: "",
      newCustomPropertyListColor: "red",
      customPropertyLists: {},
      customPropertyListColors: {},
      rows: [],
      columns: [],
      rawSearchResultProperties: [],
      mapBounds: {},
      zipCode: null,
      loading: false,
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
          list.map((v) => ({
            ...v,
            color: this.customPropertyListColors[key],
          }))
        );
      }
      return properties.flat();
    },
    allProperties() {
      let properties = this.customProperties.slice();
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
        this.zipCode,
        this.searchBy,
        this.selectedBuildingTypes
      ).then(
        (results) => (
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
      this.selectedMarkers.forEach((marker) =>
        this.addToSelectedPropertyList(this.activeTabPane, marker)
      );
    },
    addToSelectedPropertyList(listName, property) {
      let thisProperty = this.propertyDict[property.parcelNumber];
      thisProperty["color"] = this.customPropertyListColors[listName];
      this.customPropertyLists[listName].push(thisProperty);

      this.customPropertyLists[listName] = [
        ...new Set(this.customPropertyLists[listName]),
      ];

      // Convert {'list1': [{parcel: 102}, {parcel: 103}]}
      // to {'list1': [102, 103]}
      let customPropertyParcelNumberDict = {};
      Object.entries(this.customPropertyLists).map(function(entry) {
        customPropertyParcelNumberDict[entry[0]] = entry[1].map(
          (x) => x.parcel_number
        );
        return customPropertyParcelNumberDict;
      });
      this.$router.replace({
        name: "Neighborhoods",
        query: {
          ...customPropertyParcelNumberDict,
        },
      });
    },
  },
  created() {
    this.mapBounds = {
      _northEast: { lat: 39.977523, lng: -75.136808 },
      _southWest: { lat: 39.922655, lng: -75.193699 },
    };
    // Get the property list from the parcel numbers
    this.loading = true;
    getNeighborhoodsPageFromParcelNumbers(this.$route.query).then(
      (results) => (
        (this.customPropertyLists = results.saved_properties),
        (this.customPropertyListColors = this.setColorsAndUrlToSavedPropertyLists(
          Object.keys(results.saved_properties)
        )),
        (this.loading = false)
      )
    );
  },
};
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
