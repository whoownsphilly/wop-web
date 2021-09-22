<template>
  <div class="about">
    <p>Over the last several years, cities have begun open sourcing a variety of previously difficult to access data, including property, deed, violations, evictions, and other information related to housing. This has allowed community members to build tools on top of the data for a variety of purposes.</p>

<p>Recently, in many cities, one of the purposes that has arisen is allowing people to look up who actually owns which rental properties. This information is both extremely valuable and fairly difficult to organize.</p>

<p>This information is valuable for several reasons:</p>
<sui-list>
<sui-list-item><b>Legal:</b> it can be used for legal purposes for tenants and their advocates</sui-list-item>
<sui-list-item><b>Organizing:</b> it can be used to see what other properties a landlord owns and what other violations may be on their record</sui-list-item>
<sui-list-item><b>Enforcement:</b> government officials can use this information to track bad landlords, better enforce laws, and escalate violations</sui-list-item>
<sui-list-item><b>Policy:</b> journalists and academics can use this information in different ways: which neighborhoods are being preyed on, which landlords are under investigation for other citations, etc.</sui-list-item>
</sui-list>

<p>This information is difficult to organize for several reasons:</p>
<sui-list>
<sui-list-item><b>Multiple sources:</b> There are different datasets for different types of data, and the link between these datasets is not always documented or easily discoverable.</sui-list-item>
<sui-list-item><b>Messy/incomplete data:</b> Either due to incompetence or nefarious reasons, there are many examples of data that are incomplete or straight up wrong (data in the wrong field, truncated names, misspellings that make it difficult to group data together).</sui-list-item>
<sui-list-item><b>Difficult/misapplied interface:</b> While cities do make this data available, and even build websites to search through the data, the interfaces are not structured for the purposes above, and sometimes become overly restrictive when the city learns about some of the previously described use cases (for example Philly now prevents direct “search by owner”).</sui-list-item>
<sui-list-item><b>Purposely hidden identities:</b> Landlords who own properties typically use shell companies, LLCs, and other business structures to hide their true identity. This makes it difficult to get a full picture of a landlord’s housing portfolio.</sui-list-item>
</sui-list>
<h2>Similar Websites</h2>
<p>Luckily, lots of people are working on addressing these issues!</p>

<p>Here is a running list of websites that use open data to make it easier to find landlords:</p>
<ul>
    <li><a href="http://www.philly-landlord-spotter.com" target="_blank">Philly-landlord-spotter.com (Philadelphia)</a></li>
    <li><a href="http://phillypropertylookup.herokuapp.com/" target="_blank">phillypropertylookup.herokuapp.com (Philadelphia)</a></li>
    <li><a href="https://propertyowners.phl.party/" target="_blank">https://propertyowners.phl.party/ (Philadelphia)</a></li>
    <li><a href="https://whoownswhat.justfix.nyc" target="_blank">WhoOwnsWhat (NYC)</a></li>
    <li><a href="https://portal.displacementalert.org" target="_blank">Displacement Alert Portal (NYC)</a></li>
    <li><a href="https://data.cityofchicago.org/Buildings/Problem-Landlord-List-Map/dip3-ud6z" target="_blank">City of chicago problem landlord list (Chicago)</a></li>
    <li><a href="https://findmylandlord.chicagodsa.org/" target="_blank">Find My Landlord (Chicago)</a></li>
    <li><a href="https://antievictionmap.com/" target="_blank">Anti-Eviction Mapping Project (Bay Area)</a></li>
    <li><a href="https://www.ownit.la/own-it-public#14/34.03835/-118.23905" target="_blank">Own It (LA)</a></li>
    <li><a href="https://rentsmart.boston.gov/index.html" target="_blank">RentSmart (Boston)</a></li>
    <li><a href="https://www.tenantpower.org/" target="_blank">Tenant Power (Boston area)</a></li>
    <li><a href="https://app.pittsburghhousing.org/" target="_blank">https://app.pittsburghhousing.org/ (Pittsburgh)</a></li>
    <li><a href="https://ownersearch.pittsburghhousing.org/" target="_blank">https://ownersearch.pittsburghhousing.org/ (Pittsburgh)</a></li>
    <li><a href="http://tools.wprdc.org/property-dashboard/" target="_blank">http://tools.wprdc.org/property-dashboard/ (Pittsburgh)</a></li>
    </ul>
  </div>
</template>
<style>
.about {
  padding: 50px;
}
</style>
