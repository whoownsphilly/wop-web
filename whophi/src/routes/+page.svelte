
<script lang="ts">
    /* HANDLING THE INPUT */
    import axios from "axios";
    import { goto } from '$app/navigation';

    let searchInput; // use with bind:this to focus element
    let inputValue = "";
    let filteredItems = [];

    const domain = "http://localhost:8081/"
    const filterItems = async () => {
        if (inputValue && inputValue.length > 3) {
            const endpoint = `${domain}api/v1/autocomplete?startswith_str=${inputValue.toLowerCase()}`

            const result = await axios.get(endpoint)
            filteredItems = result.data.results
        }
    }

    const selectItem = (item) => {
        //const selectionIndex = item["url"];
        // let selectedResult = filteredItems[selectionIndex];

        // Save the selection to vuex so it can be referenced later.
        // this.$store.dispatch("updateSelectedResult", selectedResult);

        let selectedParcelNumber = item["opa_account_num"];
        goto(`/property/${selectedParcelNumber}`, { replaceState: true })
    }
</script>

<main class="flex flex-col items-center h-screen pt-36 p-4">

    <h1 class="text-4xl text-bold text-emerald-800">Who Owns Philly?</h1>
    <p class="text-center">  Find out who owns what in Philly, what else
        they might own in the city, and information about their properties.</p>

        <div class=" py-8 flex w-full lg:w-1/2 flex-col items-center">
            <input class="py-4 px-8 w-full rounded-full border text-xl"
                   type="text"
                   placeholder="Search address or owner..."
                   bind:this={searchInput}
                   bind:value={inputValue}
                   on:input={filterItems}>
            {#if filteredItems.length > 0}
                <ul class="relative mt-2 w-full border divide-y shadow-md rounded-lg">
                    {#each filteredItems as item}
                        <li class="p-2 hover:bg-emerald-200 hover:cursor-pointer" on:click={() =>selectItem(item)}>
                            {item.computed_location}
                        </li>
                    {/each}
                </ul>
            {/if}
            <div class="text-center">
                Enter a <b>Philly address</b>, <b>landlord's name</b>, or <b>property manager</b>.
            </div>
        </div>
    <div class="w-3/4 flex flex-col items-center gap-4">
        <p class="text-center">
            <b>Is the address not showing up?</b> Search for the address on
            <a href="https://atlas.phila.gov">atlas.phila.gov</a> to see how the
            City formats addresses and owner names. We try our best to match
            addresses to the City’s format, but sometimes the City formats addresses
            in ways we can't detect.
        </p>
    </div>



</main>
