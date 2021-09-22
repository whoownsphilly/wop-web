<template>
  <div class="property">
    <div v-if="loading">
      <sui-dimmer active inverted>
        <sui-loader :content="loadingContent" />
      </sui-dimmer>
    </div>
    <div v-else class="dashboard">
      <div class="propertyHeader">
        <sui-statistic horizontal>
          <sui-statistic-value>{{
            propertyResult.location
          }}</sui-statistic-value>
          <sui-statistic-label> is likely owned by</sui-statistic-label>
        </sui-statistic>
        <sui-statistic horizontal>
          <sui-statistic-value>
            <span v-tooltip.bottom="propertySourceString"
              >{{ latestOwnerString }}<sup>*</sup></span
            ></sui-statistic-value
          >
        </sui-statistic>
      </div>
      <sui-grid celled>
        <sui-grid-row>
          <sui-grid-column :width="6">
            <div style="font-size: 18px">
              The owner of this property is associated with
              <b>{{ uniqueProperties.length }}</b> properties valued at
              <b>{{ totalValueOfProperties }}</b
              >.
            </div>
            <leaflet-map
              :latLngs="properties"
              :highlightedLatLng="propertyResult"
            />
          </sui-grid-column>
          <sui-grid-column :width="4">
            <sui-container text>
              <p>
                {{ buildingDescription }}.
                <span v-if="latestTransaction !== null">
                  This property was purchased from
                  <b>{{ latestTransaction.grantors }}</b> on
                  <b>{{ latestTransaction.receipt_date | luxon }}</b>.
                  <span v-if="latestRentalLicense !== null">
                      <br><br>The status of the latest rental license is:
                      <b>{{ latestRentalLicense.licensestatus }}</b>, it was
                      initially issued on <b>{{ latestRentalLicense.initialissuedate | luxon }}</b>
                      with expiration of <b>{{latestRentalLicense.expirationdate | luxon }}</b>.
                  </span>
                  <span v-else>
                      There were no rental licenses found for this address.
                  </span>
                </span>
              </p>
              <sui-accordion>
                <sui-accordion-title>
                  <sui-icon name="dropdown" />
                  Connected Possible Owners ({{ fullOwnersList.length }})
                </sui-accordion-title>
                <sui-accordion-content>
                  <span v-for="(owner, i) in fullOwnersList" :key="i">
                    - {{ owner.owner_name }}, Relation Score: {{ owner.score
                    }}<br />
                  </span>
                </sui-accordion-content>
              </sui-accordion>
              <h3>
                Top {{ numResultsString(this.complaints) }} most common 311
                complaints by owner
              </h3>
              <p v-if="complaints !== null">
                <span v-if="complaints.rows.length === 0">
                  No complaints filed.
                </span>
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
              <h3>
                Top {{ numResultsString(this.violations) }} most common
                violations by owner
              </h3>
              <p v-if="violations !== null">
                <span v-if="violations.rows.length === 0">
                  No violations filed.
                </span>
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
              <router-link to="/info" class="ui button positive" tag="button"
                >Click to take action!</router-link
              >
              <sui-divider horizontal
                >Crowd-Sourced Owner Information</sui-divider
              >
              <h4>
                Crowd-Sourced Information for properties with mailing address:
                {{ propertyResult.mailing_street }}
                {{ propertyResult.mailing_address_1 }}
              </h4>
              <historical-crowd-sourced-tab
                :mailingStreet="propertyResult.mailing_street || ''"
                :mailingAddress1="propertyResult.mailing_address_1 || ''"
              />
              <div v-if="$siteMode.mode !== 'basic'">
                <h2 is="sui-header">Links</h2>
                <a :href="propertyResult.link_atlas" target="_blank"
                  >Link to Atlas</a
                ><br />
                <a
                  :href="propertyResult.link_cyclomedia_street_view"
                  target="_blank"
                  >Link to Cyclomedia Street View</a
                ><br />
                <a
                  :href="propertyResult.link_property_phila_gov"
                  target="_blank"
                  >Link to property.phila.gov</a
                ><br />
                <a
                  :href="propertyResult.link_license_inspections"
                  target="_blank"
                  >Link to li.phila.gov</a
                >
              </div>
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
      latestTransaction: null,
      propertySourceString: "based on the latest property assessment.",
      complaints: null,
      violations: null,
      latestRentalLicense: null,
      fullOwnersList: []
    };
  },
  computed: {
    latestOwnerString() {
      if (this.latestTransaction !== null) {
        return (
          this.latestTransaction.grantees + " " + (this.latestTransaction.legal_remarks || "")
        );
      } else {
        return this.owners;
      }
    },
    loadingContent() {
      return (
        "Finding all " +
        this.loadingStep +
        " related information (may take some time)..."
      );
    },
    uniqueProperties() {
      let uniqueParcelNumbers = new Set();
      let uniqueProperties = [];
      this.properties.forEach(property => {
        if (!uniqueParcelNumbers.has(property.parcel_number)) {
          uniqueProperties.push(property);
        }
        uniqueParcelNumbers.add(property.parcel_number);
      });
      return uniqueProperties;
    },
    totalValueOfProperties() {
      let totalValue = 0;
      this.uniqueProperties.forEach(function(row) {
        totalValue += row.market_value;
      });
      var formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      });
      return formatter.format(totalValue).slice(0, -3);
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
      if ((this.propertyResult !== null) & (this.latestGrantees !== null)) {
        if (this.propertyResult.owner_1) {
          ownerList.push(this.propertyResult.owner_1);
        }
        if (this.propertyResult.owner_2) {
          ownerList.push(this.propertyResult.owner_2);
        }
      }
      return ownerList.join();
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
  methods: {
    numResultsString(theseResults) {
      if (theseResults && theseResults.rows.length > 0) {
        return Math.min(theseResults.rows.length, 5);
      } else {
        return "";
      }
    }
  },
  async created() {
    this.loading = true;
    this.loadingStep = "property";
    // To do, just join this to a deeds query to get both
    const data = await getTableInfo(
      "properties",
      "parcel_number",
      this.parcelNumber
    );
    const licensesData = await getTableInfo(
      "licenses",
      "parcel_number",
      this.parcelNumber
    );
    if ("results" in licensesData) {
      let sortedData = licensesData.results.rows;
      sortedData = sortedData.sort((a, b) =>
        a.initialissuedate > b.initialissuedate ? 1 : -1
      );
      sortedData = sortedData.filter(
        a =>
          a.licensetype === "Rental"
      );
      if(sortedData.length > 0){
      this.latestRentalLicense = sortedData[0]
      }
    }
    const deedData = await getTableInfo(
      "real_estate_transfers",
      "parcel_number",
      this.parcelNumber
    );
    if ("results" in deedData) {
      let prevEndDate = null;
      let sortedData = deedData.results.rows;
      sortedData = sortedData.sort((a, b) =>
        a.recording_date > b.recording_date ? 1 : -1
      );
      sortedData = sortedData.filter(
        a =>
          a.document_type === "DEED" ||
          a.document_type === "DEED SHERIFF" ||
          a.document_type === "DEED OF CONDEMNATION" ||
          a.document_type === "DEED MISCELLANEOUS" ||
          a.document_type === " DEED LAND BANK"
      );
      for (let i in sortedData) {
        let row = sortedData[i];
        row.name = row.grantors;
        if (i == 0) {
          row.start = new Date(
            row.year_built !== "0000" ? row.year_built : row.receipt_date
          );
        } else {
          row.start = new Date(Date.parse(prevEndDate));
        }
        row.end = new Date(Date.parse(row.receipt_date));
        prevEndDate = row.end;
        this.latestTransaction = row;
        this.propertySourceString = "based on the latest deed transfer.";
      }
    }
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
<style>
.propertyHeader {
  text-align: center;
  font-size: 16px;
}
.dashboard {
  margin: 30px;
}
</style>
