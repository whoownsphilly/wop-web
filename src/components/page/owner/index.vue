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
            <owner-portfolio
              :properties="currentProperties"
              :mailingAddressBasedOwnerPortfolio="
                mailingAddressBasedOwnerPortfolioInfo
              "
              :ownerBasedOwnerPortfolio="ownerBasedOwnerPortfolioInfo"
            />
          </sui-grid-column>
        <sui-grid-column :width="10">
    <sui-statistics-group horizontal>
      <sui-statistic in-group>
        <sui-statistic-value>13</sui-statistic-value>
        <sui-statistic-label>Properties Owned
          </sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>5.5</sui-statistic-value>
        <sui-statistic-label>years of average property ownership 
          </sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>$139,000,000</sui-statistic-value>
        <sui-statistic-label>Total Value of Properties
          </sui-statistic-label
        >
      </sui-statistic>
      <sui-statistic in-group>
        <sui-statistic-value>10</sui-statistic-value>
        <sui-statistic-label>Violations Since 2015
          </sui-statistic-label
        >
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
              <sui-accordion-title>
                <sui-icon name="dropdown" />
                Property Ownership Timeline
              </sui-accordion-title>
              <sui-accordion-content>
                <h2>Property Timeline</h2>
                <vue-apex-timeline
                  :data="ownerBasedPropertyTimelineData"
                  labelCol="location_unit"
                  startCol="start_dt"
                  endCol="end_dt"
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
import VueApexTimeline from "@/components/ui/charts/Timeline";
import VueApexBarChart from "@/components/ui/charts/BarChart";
import DataTable from "@/components/ui/DataTable";
import SingleColumnDataTable from "@/components/ui/SingleColumnDataTable";
import { formatCurrencyValue } from "@/components/utils/formatting.js";

export default {
  name: "HistoricalOwnerTab",
  components: {
    VueApexTimeline,
    VueApexBarChart,
    DataTable,
    SingleColumnDataTable,
    OwnerPortfolio
  },
  props: {
    ownerName: {
      type: String,
      required: true
    },
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
      ownerBasedNUniqueProperties: null,
      ownerBasedPropertyTimelineData: [],
      ownerBasedOwnerPropertyCountsByName: [],
      ownerBasedTotalValue: null,
      mailingAddress: null,
      mailingAddressBasedNames: null,
      mailingAddressBasedOwnerPortfolioInfo: null,
      mailingAddressBasednUniqueProperties: null,
      mailingAddressBasedPropertyTimelineData: [],
      mailingAddressBasedOwnerPropertyCountsByName: [],
      mailingAddressBasedTotalValue: null
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
      // Some overly complicated logic to get a list of unique properties
      var allProperties = this.ownerBasedCurrentProperties.concat(
        this.mailingAddressBasedCurrentProperties
      );
      var allUniqueProperties = [];
      var allUniquePropertyParcelNumbers = [];
      for (var i = 0; i < allProperties.length; i++) {
        if (
          !allUniquePropertyParcelNumbers.includes(
            allProperties[i].opa_account_num
          )
        ) {
          allUniquePropertyParcelNumbers.push(allProperties[i].opa_account_num);
          allUniqueProperties.push(allProperties[i]);
        }
      }
      return allUniqueProperties;
    },
    isPageStillLoading() {
      return this.ownerLoading || this.mailingAddressLoading;
    }
  },
  methods: {
    getFormattedCurrency(value) {
      return formatCurrencyValue(value);
    }
  },
  created() {
    this.ownerLoading = true;
    this.mailingAddressLoading = true;
    // get all time-based data for the last year
    getOwnerPageInfoByName(this.parcelNumber, this.ownerName).then(
      propertyResults => {
        this.ownerBasedPropertyTimelineData =
          propertyResults["results"]["timeline"];
        this.ownerBasedNames = propertyResults["results"]["alias_names"];
        this.ownerBasedCurrentProperties =
          propertyResults["results"]["current_properties"];
        this.ownerBasedNUniqueProperties =
          propertyResults["results"]["n_unique_properties"];
        this.ownerBasedOwnerPropertyCountsByName =
          propertyResults["display_inputs"]["owner_property_counts_by_name"];
        this.ownerBasedTotalValue = propertyResults["results"]["total_value"];
        this.ownerBasedOwnerPortfolioInfo =
          propertyResults["display_inputs"]["owner_portfolio_text"];
        this.ownerLoading = false;
      }
    );
    getOwnerPageInfoByMailingAddress(this.parcelNumber).then(
      propertyResults => {
        this.mailingAddress = propertyResults["metadata"]["mailing_address"];
        this.mailingAddressBasedNames =
          propertyResults["results"]["alias_names"];
        this.mailingAddressBasedPropertyTimelineData =
          propertyResults["results"]["timeline"];
        this.mailingAddressBasedCurrentProperties =
          propertyResults["results"]["current_properties"];
        this.mailingAddressBasedNUniqueProperties =
          propertyResults["results"]["n_unique_properties"];
        this.mailingAddressBasedOwnerPropertyCountsByName =
          propertyResults["display_inputs"]["owner_property_counts_by_name"];
        this.mailingAddressBasedOwnerPortfolioInfo =
          propertyResults["display_inputs"]["owner_portfolio_text"];
        this.mailingAddressBasedTotalValue =
          propertyResults["results"]["total_value"];
        this.mailingAddressLoading = false;
      }
    );
  }
};
</script>
