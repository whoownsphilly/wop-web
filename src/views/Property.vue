<template>
  <div class="property">
    <div v-if="loading">
      <sui-dimmer active inverted>
        <sui-loader :content="loadingContent" />
      </sui-dimmer>
    </div>
    <div v-else>
      <sui-grid celled>
        <sui-grid-row>
          <sui-grid-column :width="6">
            <leaflet-map
              :latLngs="properties"
              :highlightedLatLng="propertyResult"
            />
          </sui-grid-column>
          <sui-grid-column :width="4">
            <sui-container text>
              <h2 is="sui-header">
                {{ propertyResult.location }} {{ propertyResult.unit }}
              </h2>
              <p>{{ buildingDescription }}</p>
              <h3>Top 5 most common 311 complaints by owner</h3>
              <p v-if="complaints">
                <span
                  v-for="(complaintByName, i) in complaints.value_counts"
                  :key="i"
                >
                  <span v-if="i < 5">
                    - {{ complaintByName.complaintcodename }}:
                    {{ complaintByName.count }}<br />
                  </span>
                </span>
              </p>
              <p v-else>Loading...</p>
              <h3>Top 5 most common violations by owner</h3>
              <p v-if="violations">
                <span
                  v-for="(violationByTitle, i) in violations.value_counts"
                  :key="i"
                >
                  <span v-if="i < 5">
                    - {{ violationByTitle.violationcodetitle }}:
                    {{ violationByTitle.count }}<br />
                  </span>
                </span>
              </p>
              <p v-else>Loading...</p>
              <h2 v-for="owner in owners" :key="owner">
                Owner(s): {{ owner }}
              </h2>
              <h2>
                This portfolio is associated with
                {{ numberOfUniqueProperties }} properties
              </h2>
              <sui-accordion>
                <sui-accordion-title>
                  <sui-icon name="dropdown" />
                  Related Owners ({{ fullOwnersList.length }})
                </sui-accordion-title>
                <sui-accordion-content>
                  <span v-for="(owner, i) in fullOwnersList" :key="i">
                    - {{ owner.owner_name }}, Relation Score: {{ owner.score
                    }}<br />
                  </span>
                </sui-accordion-content>
              </sui-accordion>
              <h4>Crowd-Sourced Information for properties with mailing address: {{propertyResult.mailing_street }} {{ propertyResult.mailing_address_1 }}</h4> 
              <historical-crowd-sourced-tab
                :mailingStreet="propertyResult.mailing_street"
                :mailingAddress1="propertyResult.mailing_address_1"
              />
              <h2 is="sui-header">Links</h2>
              <a :href="propertyResult.link_atlas" target="_blank"
                >Link to Atlas</a
              ><br />
              <a
                :href="propertyResult.link_cyclomedia_street_view"
                target="_blank"
                >Link to Cyclomedia Street View</a
              ><br />
              <a :href="propertyResult.link_property_phila_gov" target="_blank"
                >Link to property.phila.gov</a
              ><br />
              <a :href="propertyResult.link_license_inspections" target="_blank"
                >Link to li.phila.gov</a
              >
            </sui-container>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
      <sui-tab v-if="$siteMode.mode !== 'basic'">
        <sui-tab-pane title="Historical Property Info">
          <historical-property-tab :parcelNumber="this.parcelNumber" />
        </sui-tab-pane>
        <sui-tab-pane v-for="owner in owners" :key="owner" :title="owner">
          <historical-owner-tab
            :owner="owner"
            :highlightedProperty="propertyResult"
          />
        </sui-tab-pane>
        <sui-tab-pane title="Mailing Address">
          <mailing-address-tab
            :mailingStreet="mailingStreetOrLocation"
            :mailingAddress1="mailingAddress1"
          />
        </sui-tab-pane>
        <sui-tab-pane title="Crowd-Sourced Info">
          <historical-crowd-sourced-tab
            :mailingStreet="mailingStreetOrLocation"
            :mailingAddress1="mailingAddress1"
          />
        </sui-tab-pane>
      </sui-tab>
    </div>
  </div>
</template>

<script>
import HistoricalPropertyTab from "@/components/HistoricalPropertyTab";
import HistoricalOwnerTab from "@/components/HistoricalOwnerTab";
import HistoricalCrowdSourcedTab from "@/components/HistoricalCrowdSourcedTab";
import LeafletMap from "@/components/LeafletMap";
import MailingAddressTab from "@/components/MailingAddressTab";
import { getTableInfo } from "@/api/singleTable";
import { getOwnersTimelineTableInfo } from "@/api/singleTable";

export default {
  name: "Property",
  components: {
    LeafletMap,
    HistoricalPropertyTab,
    HistoricalOwnerTab,
    HistoricalCrowdSourcedTab,
    MailingAddressTab
  },
  data() {
    return {
      loading: false,
      loadingStep: "",
      parcelNumber: this.$route.params.parcelNumber,
      propertyResult: null,
      properties: [],
      complaints: [],
      violations: [],
      fullOwnersList: []
    };
  },
  computed: {
    loadingContent() {
      return (
        "Finding all " +
        this.loadingStep +
        " related information (may take some time)..."
      );
    },
    numberOfUniqueProperties() {
      let uniqueParcelNumbers = new Set();
      this.properties.forEach(property => {
        uniqueParcelNumbers.add(property.parcel_number);
      });
      return uniqueParcelNumbers.size;
    },
    mailingStreetOrLocation() {
      if (this.propertyResult !== null) {
        return (
          this.propertyResult.mailing_street || this.propertyResult.location
        );
      }
      return "";
    },
    mailingAddress1() {
      if (this.propertyResult !== null) {
        return this.propertyResult.mailing_address_1;
      }
      return "";
    },
    owners() {
      const ownerList = [];
      if (this.propertyResult !== null) {
        if (this.propertyResult.owner_1) {
          ownerList.push(this.propertyResult.owner_1);
        }
        if (this.propertyResult.owner_2) {
          ownerList.push(this.propertyResult.owner_2);
        }
      }
      return ownerList;
    },
    buildingDescription() {
      let year_built_estimate_str = "";
      if (this.propertyResult.year_built_estimate === "Y") {
        year_built_estimate_str = " (although this is an estimate)";
      }
      if (this.propertyResult !== null) {
        return (
          "This building was constructed in " +
          this.propertyResult.year_built +
          year_built_estimate_str +
          ", and is described as a " +
          this.propertyResult.category_code_description +
          ", " +
          this.propertyResult.building_code_description
        );
      }
      return "";
    }
  },
  async created() {
    this.loading = true;
    this.loadingStep = "property";
    const data = await getTableInfo(
      "properties",
      "parcel_number",
      this.parcelNumber
    );
    if ("results" in data && data.results.rows.length == 1) {
      this.propertyResult = data.results.rows[0];
      this.address = this.propertyResult.location;
      this.highlightedLatLng = {
        lat: this.propertyResult.lat,
        lng: this.propertyResult.lng
      };
      this.loadingStep = "owner timeline";
    }
    // Owner-Based Data
    const ownerRelatedPropertyData = await getOwnersTimelineTableInfo(
      this.propertyResult.owner_1
    );
    if (ownerRelatedPropertyData.success) {
      ownerRelatedPropertyData.owner_timeline.forEach(row => {
        row["color"] = "yellow";
        row["relation"] = "owner";
        this.properties.push(row);
      });
      this.fullOwnersList = ownerRelatedPropertyData.owners_list;
      this.loadingStep = "mailing address";
    }
    // Mailing Address-Based Data
    const mailingAddressData = await getTableInfo(
      "properties",
      "location_by_mailing_address",
      this.propertyResult.location
    );
    if (mailingAddressData.results.rows) {
      mailingAddressData.results.rows.forEach(row => {
        row["color"] = "red";
        row["relation"] = "mailing_address";
        this.properties.push(row);
      });
      this.loadingStep = "complaints";
    }
    this.loading = false;

    // Owner-based complaints data
    let complaintsResult = await getTableInfo(
      "complaints",
      "owner",
      this.propertyResult.owner_1,
      ["complaintcodename"]
    );
    // Owner-based violations data
    let violationsResult = await getTableInfo(
      "violations",
      "owner",
      this.propertyResult.owner_1,
      ["violationcodetitle"]
    );
    if (complaintsResult.results.rows) {
      this.complaints = complaintsResult.results;
    }
    if (violationsResult.results.rows) {
      this.violations = violationsResult.results;
    }
  }
};
</script>
