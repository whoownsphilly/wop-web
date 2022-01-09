<template>
  <div>
    <h3>De-select owner names that aren't relevant.</h3>
    <span v-for="ownerName in ownersList" :key="ownerName.owner_name">
      <sui-button
        :content="ownerName.owner_name"
        toggle
        :active="!isInactive[ownerName.owner_name]"
        @click="changeActiveOwners"
      />
    </span>
  </div>
</template>

<script>
export default {
  name: "OwnerSelector",
  props: {
    ownersList: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      isInactive: {}
    };
  },
  methods: {
    changeActiveOwners(thisButton) {
      const thisButtonName = thisButton.srcElement.innerText;
      this.isInactive[thisButtonName] = !this.isInactive[thisButtonName];
      this.isInactive.__ob__.dep.notify(); //I know this is hacky but I'm learning.
    }
  }
};
</script>
