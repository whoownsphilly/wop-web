<template>
  <div>
    <div v-if="isPageStillLoading">
      <sui-dimmer active inverted>
        <sui-loader
          content="Finding All Information for this owner. This may take up to 30 seconds..."
        />
      </sui-dimmer>
    </div>
    <div v-else>
      <sui-grid>
        <sui-grid-row>
          <sui-grid-column :width="6">
            <owner-portfolio :properties="currentProperties" />
          </sui-grid-column>
          <sui-grid-column :width="10">
            <div>Mailing Address: {{ mailingAddress }}</div>
            <sui-statistics-group horizontal>
              <sui-statistic in-group>
                <sui-statistic-value>{{
                  currentProperties.length
                }}</sui-statistic-value>
                <sui-statistic-label
                  >Properties Currently Associated with
                  owner</sui-statistic-label
                ><sup
                  ><info-modal modalName="owner.portfolio.propertyCount"
                /></sup>
              </sui-statistic>
              <sui-statistic in-group>
                <sui-statistic-value>{{
                  getFormattedCurrency(totalAssessedValue)
                }}</sui-statistic-value>
                <sui-statistic-label
                  >Total Value of Properties</sui-statistic-label
                ><sup
                  ><info-modal modalName="owner.portfolio.marketValueInfo"
                /></sup>
              </sui-statistic>
              <sui-statistic in-group>
                <sui-statistic-value>{{ nViolationsOpen }}</sui-statistic-value>
                <sui-statistic-label
                  >Open Violations across properties currently associated with
                  owner </sui-statistic-label
                ><sup
                  ><info-modal modalName="owner.portfolio.nOpenViolations"
                /></sup>
              </sui-statistic>
              <sui-statistic in-group>
                <sui-statistic-value>{{
                  nViolationsClosed
                }}</sui-statistic-value>
                <sui-statistic-label
                  >Violations since
                  {{ violationsComplaintsDateSince | luxon }} across properties
                  currently associated with owner </sui-statistic-label
                ><sup
                  ><info-modal modalName="owner.portfolio.nClosedViolations"
                /></sup>
              </sui-statistic>
              <sui-statistic in-group>
                <sui-statistic-value>{{ nComplaints }}</sui-statistic-value>
                <sui-statistic-label
                  >Complaints since
                  {{ violationsComplaintsDateSince | luxon }} across properties
                  currently associated with owner </sui-statistic-label
                ><sup
                  ><info-modal modalName="owner.portfolio.nComplaints"
                /></sup>
              </sui-statistic>
            </sui-statistics-group>
            <sui-accordion exclusive styled>
              <sui-accordion-title>
                <sui-icon name="dropdown" />
                Owner-based Properties:
                {{ ownerBasedCurrentProperties.length }}/{{
                  currentProperties.length
                }}
              </sui-accordion-title>
              <sui-accordion-content>
                <single-column-data-table
                  :rows="ownerBasedNames"
                  title="Aliases"
                />
                <h2>Property Ownership Timeline Table</h2>
                <data-table
                  :rows="ownerBasedPropertyTimelineData"
                  :columns="ownerBasedPropertyTimelineDataColumns"
                  title="Owner Timeline"
                />
                <vue-apex-bar-chart
                  :data="ownerBasedOwnerPropertyCountsByName"
                />
              </sui-accordion-content>
              <sui-accordion-title>
                <sui-icon name="dropdown" />
                Mailing Address-based Properties:
                {{ mailingAddressBasedCurrentProperties.length }}/{{
                  currentProperties.length
                }}
              </sui-accordion-title>
              <sui-accordion-content>
                <single-column-data-table
                  :rows="mailingAddressBasedNames"
                  title="Aliases"
                />
                <h2>Mailing-Address Ownership Timeline Table</h2>
                <data-table
                  :rows="mailingAddressBasedPropertyTimelineData"
                  :columns="mailingAddressBasedPropertyTimelineDataColumns"
                  title="Mailing Address Timeline"
                />
                <vue-apex-bar-chart
                  :data="mailingAddressBasedOwnerPropertyCountsByName"
                />
              </sui-accordion-content>
            </sui-accordion>
          </sui-grid-column>
        </sui-grid-row>
      </sui-grid>
    </div>
  </div>
</template>

<script>
import {
  getOwnerPageInfoByName,
  getOwnerPageInfoByMailingAddress
} from "@/api/pages";
import OwnerPortfolio from "@/components/page/owner/Portfolio";
import VueApexBarChart from "@/components/ui/charts/BarChart";
import DataTable from "@/components/ui/DataTable";
import SingleColumnDataTable from "@/components/ui/SingleColumnDataTable";
import { formatCurrencyValue } from "@/components/utils/formatting.js";

export default {
  name: "HistoricalOwnerTab",
  components: {
    VueApexBarChart,
    DataTable,
    SingleColumnDataTable,
    OwnerPortfolio
  },
  props: {
    parcelNumber: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      aliasNameColumns: [{ label: "alias", name: "alias" }],
      ownerLoading: false,
      mailingAddressLoading: false,
      ownerBasedNames: null,
      ownerBasedOwnerPortfolioInfo: null,
      ownerBasedPropertyTimelineData: [],
      ownerBasedOwnerPropertyCountsByName: [],
      mailingAddress: null,
      mailingAddressBasedNames: null,
      mailingAddressBasedOwnerPortfolioInfo: null,
      mailingAddressBasedPropertyTimelineData: [],
      mailingAddressBasedOwnerPropertyCountsByName: [],
      violationsComplaintsDateSince: "2007-01-01"
    };
  },
  computed: {
    ownerBasedPropertyTimelineDataColumns() {
      if (this.ownerBasedPropertyTimelineData.length > 0) {
        return Object.keys(this.ownerBasedPropertyTimelineData[0]).map(col => {
          return { label: col, field: col };
        });
      } else {
        return [];
      }
    },
    mailingAddressBasedPropertyTimelineDataColumns() {
      if (this.mailingAddressBasedPropertyTimelineData.length > 0) {
        return Object.keys(this.mailingAddressBasedPropertyTimelineData[0]).map(
          col => {
            return { label: col, field: col };
          }
        );
      } else {
        return [];
      }
    },
    currentProperties() {
      return this.loadedCompiledData.currentProperties;
    },
    nViolationsOpen() {
      return this.loadedCompiledData.nViolationsOpen;
    },
    nViolationsClosed() {
      return this.loadedCompiledData.nViolationsClosed;
    },
    nComplaints() {
      return this.loadedCompiledData.nComplaints;
    },
    totalAssessedValue() {
      return this.loadedCompiledData.marketValue;
    },
    ownerBasedCurrentProperties() {
      return this.ownerBasedPropertyTimelineData.filter(function(el) {
        return el.current_owner;
      });
    },
    mailingAddressBasedCurrentProperties() {
      return this.mailingAddressBasedPropertyTimelineData.filter(function(el) {
        return el.current_owner;
      });
    },
    loadedCompiledData() {
      if (!this.ownerLoading && !this.mailingAddressLoading) {
        var allUniqueCurrentProperties = [];
        var nViolationsOpen = 0;
        var nViolationsClosed = 0;
        var nComplaints = 0;
        var marketValue = 0;
        let allProperties = this.ownerBasedPropertyTimelineData.concat(
          this.mailingAddressBasedPropertyTimelineData
        );
        var allUniquePropertyParcelNumbers = [];
        for (var i = 0; i < allProperties.length; i++) {
          let thisProperty = allProperties[i];
          if (
            !allUniquePropertyParcelNumbers.includes(
              thisProperty.opa_account_num
            )
          ) {
            allUniquePropertyParcelNumbers.push(thisProperty.opa_account_num);
            nViolationsOpen += thisProperty.n_violations_open;
            nViolationsClosed += thisProperty.n_violations_closed;
            nComplaints += thisProperty.n_complaints;
            marketValue += thisProperty.market_value;
            if (thisProperty.current_owner === true) {
              allUniqueCurrentProperties.push(allProperties[i]);
            }
          }
        }
      }
      return {
        nViolationsOpen: nViolationsOpen,
        nViolationsClosed: nViolationsClosed,
        nComplaints: nComplaints,
        currentProperties: allUniqueCurrentProperties,
        marketValue: marketValue
      };
    },
    isPageStillLoading() {
      return this.ownerLoading || this.mailingAddressLoading;
    }
  },
  methods: {
    getFormattedCurrency(value) {
      // It won't let me directly call the function so I had to make a method
      return formatCurrencyValue(value);
    }
  },
  created() {
    this.ownerLoading = true;
    this.mailingAddressLoading = true;

    getOwnerPageInfoByMailingAddress(this.parcelNumber).then(
      propertyResults => {
        this.mailingAddress = propertyResults["metadata"]["mailing_address"];
        this.mailingAddressBasedNames =
          propertyResults["results"]["alias_names"];
        this.mailingAddressBasedPropertyTimelineData =
          propertyResults["results"]["timeline"];
        this.mailingAddressBasedOwnerPropertyCountsByName =
          propertyResults["display_inputs"]["owner_property_counts_by_name"];
        this.mailingAddressLoading = false;
      }
    );
    getOwnerPageInfoByName(this.parcelNumber).then(propertyResults => {
      this.ownerBasedPropertyTimelineData =
        propertyResults["results"]["timeline"];
      this.ownerBasedNames = propertyResults["results"]["alias_names"];
      this.ownerBasedOwnerPropertyCountsByName =
        propertyResults["display_inputs"]["owner_property_counts_by_name"];
      this.ownerLoading = false;
    });
  }
};
</script>
<style>
.ui.accordion .title:not(.ui) {
  font-size: 1em;
}
</style>
