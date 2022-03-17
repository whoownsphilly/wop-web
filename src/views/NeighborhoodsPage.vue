<template>
  <div style="font-size: 18px">
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
                  label="Zip Code"
                  value="zipCode"
                  v-model="searchBy"
                />
              </sui-form-field>
              <sui-form-field>
                <sui-checkbox
                  radio
                  name="search_by"
                  label="Map Boundary"
                  value="mapBoundary"
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
            placeholder="..."
          />
        </sui-grid-column>
      </sui-grid-row>
    </sui-grid>
    <sui-divider horizontal>
      <sui-button v-on:click="updatePropertyList">Update Map</sui-button>
    </sui-divider>
    <div v-if="loading === false">
      <leaflet-map-neighborhood
        :latLngs="properties"
        @updateBounds="updateBounds"
        @addProperty="addToSelectedPropertyList"
        mapStyle="height: 350px; width: 100%"
        :includeLegend="includeLegend"
      />
    </div>
    <div v-else>
      <sui-dimmer active inverted>
        <sui-loader content="Loading..." />
      </sui-dimmer>
    </div>
    <data-table :rows="properties" title="Properties" />
    <data-table :rows="selectedProperties" title="Selected Properties" />
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
      searchBy: "zipCode",
      buildingTypes: [
        { text: "abc", value: 1 },
        { text: "def", value: 2 },
      ],
      selectedBuildingTypes: [],
      includeLegend: false,
      rows: [],
      columns: [],
      properties: [],
      selectedProperties: [],
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
    propertyDict() {
      let obj = {};
      this.properties.map(function(x) {
        let parcel_number = x.parcel_number;
        obj[parcel_number] = x;
      });
      return obj;
    },
  },
  methods: {
    updateBounds(bounds) {
      this.mapBounds = bounds;
    },
    updatePropertyList() {
      this.loading = true;
      getNeighborhoodsPageInfo(
        this.mapBounds,
        this.zipCode,
        this.searchBy
      ).then(
        (results) => (
          (this.properties = results.properties), (this.loading = false)
        )
      );
    },
    addToSelectedPropertyList(property) {
      this.selectedProperties.push(this.propertyDict[property.parcelNumber]);
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
