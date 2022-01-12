<template>
  <div>
    <sui-accordion>
      <sui-accordion-title class="large">
        <sui-icon v-if="nViolationsOpen" name="dropdown" />
        {{ nViolationsOpen || 0 }} currently open violations
      </sui-accordion-title>
      <sui-accordion-content>
        ABC
      </sui-accordion-content>
      <sui-accordion-title>
        <sui-icon v-if="nViolationsOpen" name="dropdown" />
        {{ nViolationsClosedSince || 0 }} closed violations since
        {{ dateSince | luxon }}
      </sui-accordion-title>
      <sui-accordion-content></sui-accordion-content>
      <sui-accordion-title>
        <sui-icon v-if="nComplaints" name="dropdown" />
        {{ nComplaintsSince || 0 }} complaints through 311 since
        {{ dateSince | luxon }}
      </sui-accordion-title>
      <sui-accordion-content>
        ABC
      </sui-accordion-content>
    </sui-accordion>
  </div>
</template>

<script>
/*
This component takes in a list of violations and compiles it into counts and a dropdown.
*/
export default {
  name: "ViolationsComplaints",
  props: {
    nViolationsOpen: {
      type: Number,
      required: true
    },
    nViolationsClosedSince: {
      type: Number,
      required: true
    },
    nComplaintsSince: {
      type: Number,
      required: true
    },
    dateSince: {
      type: String,
      required: true
    }
  }
};
</script>
<style>
.ui.accordion .title:not(.ui) {
  font-size: 2em;
}
</style>
