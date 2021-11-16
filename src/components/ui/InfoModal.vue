<template>
<span>
        <sui-button
          class="info-modal"
          size="mini"
          circular
          icon="info"
          @click.native="disclaimerToggle"
        />
        <sui-modal v-model="disclaimerOpen">
          <sui-modal-header
            >{{ modalInfo.header }}</sui-modal-header
          >
          <sui-modal-content>
            <p><span v-html="modalInfo.text"/></p>
          </sui-modal-content>
          <sui-modal-actions>
            <sui-button positive @click.native="disclaimerToggle">
              OK
            </sui-button>
          </sui-modal-actions>
        </sui-modal>
        </span>
</template>
<script>

import modalInfoJson from '@/text/modals.json'

export default {
  name: "InfoModal",
  components: { },
  props: {
    modalName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      modalOpen: false,
      modalInfo: modalInfoJson[this.modalName],
      disclaimerOpen: false,
    }
  },
  methods: {
    toggle() {
      this.modalOpen = !this.modalOpen;
    },
    disclaimerToggle() {
      this.disclaimerOpen = !this.disclaimerOpen;
    }
  }
};
</script>
<style>
.info-modal {
    vertical-align: top !important
}
</style>
