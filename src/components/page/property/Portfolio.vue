<template>
    <div v-if="loading">
        <sui-dimmer active inverted>
            <sui-loader :content="loadingContent" />
        </sui-dimmer>
    </div>
    <div v-else>
        <div style="font-size: 18px">
          The owner of this property is currently associated with
          <b>{{ nProperties }}</b> properties valued at
          <b>{{ totalValueOfProperties }}</b
          >.
        </div>
        <leaflet-map :latLngs="properties" :highlightedLatLngs="thisProperty"/>
    </div>
</template>
<script>

import LeafletMap from "@/components/ui/LeafletMap";
import { getOwnersCurrentPropertiesMapInfo } from "@/api/pages";
import { formatCurrencyValue } from '@/components/utils/formatting.js';

export default {
  name: "PropertyPortfolio",
  components: {
    LeafletMap
  },
  props: {
    parcelNumber: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      loadingContent: "Loading data about the owner's other properties...",
      nProperties: null,
      totalValueOfProperties: null,
      properties: [],
      thisProperty: null,
    };
  },
  methods: {
  },
  async created() {
    this.loading = true;
    getOwnersCurrentPropertiesMapInfo(
        this.parcelNumber
    ).then(data => {
      this.nProperties = data.n_properties
      this.totalValueOfProperties = formatCurrencyValue(data.total_value_of_properties)
      if(data.success){
          data.owners_currently_owned_properties.forEach(row => {
            if (row['relation'] === "self"){
                this.thisProperty = row
            }
            if (row['relation'] === "owner"){
                row["color"] = "red";
            }
            else if (row['relation'] === "mailing_address"){
                row["color"] = "yellow";
            }
            this.properties.push(row);
          })
      }
      this.loading = false
    })
}
}
</script>
<style>
.dashboard {
  margin: 30px;
}
</style>
