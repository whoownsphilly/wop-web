import {Component, createSignal, For, Show} from "solid-js";
import styles, {active} from "./neighborhoods.module.css"
import NeighborhoodMap from "./components/NeighborhoodMap";
import {getNeighborhoodsPageInfo} from "../../services/apiFetcher";

const Neighborhoods: Component = () => {
    const buildingTypes =[
        { key: "Multi Family", text: "Multi Family", value: "Multi Family", isRental: false },
        { key: "Single Family", text: "Single Family", value: "Single Family", isRental: false },
        { key: "Mixed Use", text: "Mixed Use", value: "Mixed Use", isRental: false },
        { key: "Vacant Land", text: "Vacant Land", value: "Vacant Land", isRental: false },
        { key: "Industrial", text: "Industrial", value: "Industrial", isRental: false },
        { key: "Commercial", text: "Commercial", value: "Commercial", isRental: false },
        { key: "Other", text: "Other", value: "Other", isRental: true },
        { key: "Dormitories", text: "Dormitories", value: "Dormitories", isRental: true },
        { key: "Residential Dwellings", text: "Residential Dwellings", value: "Residential Dwellings", isRental: true},
        { key: "Rooming House / Boarding House", text: "Rooming/Boarding House", value: "Rooming House / Boarding House", isRental: true },
        { key: "Hotel", text: "Hotel", value: "Hotel" }
    ]

    const [numUnitsPerList, setNumUnitsPerList] = createSignal(20)
    const [numLists, setNumLists] = createSignal(5)
    const [startingAddress, setStartingAddress] = createSignal("")
    const [zipCode, setZipCode] = createSignal("")
    const [blocksFromAddress, setBlocksFromAddress] = createSignal(0)

    const [searchType, setSearchType] = createSignal("address")
    const [activeToggles, setActiveToggles] = createSignal(["rental", "no-rental", "no-condo", "no-owner"])
    const [activeBuildingTypes, setActiveBuildingTypes] = createSignal([buildingTypes[0], buildingTypes[1], buildingTypes[8]])
    const [properties, setProperties] = createSignal([])
    const [walkingLists, setWalkingLists] = createSignal([])
    const isActive = (key: string) => {
        return activeToggles().indexOf(key) > -1
    }

    const isActiveBuildingType = (value: string) => {
        return activeBuildingTypes().find((v) => v.value === value) !== undefined
    }

    const toggleActive = (key:string) => () => {
        const active = [...activeToggles()]
        const index= active.indexOf(key)
        if(index > -1) {
            active.splice(index, 1)
            setActiveToggles(active)
        } else {
            active.push(key)
            setActiveToggles(active)
        }
    }

    const toggleActiveBuildingType = (type: any) => () => {
        const active = [...activeBuildingTypes()]
        const index= active.indexOf(type)
        if(index > -1) {
            active.splice(index, 1)
            setActiveBuildingTypes(active)
        } else {
            active.push(type)
            setActiveBuildingTypes(active)
        }
    }

    const isSearchType = (key: string) => {
        return searchType() === key
    }

    // const toggleSearchType = (type: string) => {
    //     setSearchType(type)
    // }

    // const toggleSearchType = (type: string) => () => {
    //     console.log(type)
    //     setSearchType(type)
    // }

    const getActiveToggleFilterValues = (filter) =>{
        const isToggle =  activeToggles().indexOf(filter) > -1
        const isNotToggle = activeToggles().indexOf("no-" + filter) > -1
        let result = null
        if(isToggle && !isNotToggle) {
            result = true
        }
        if(isNotToggle && !isToggle) {
            result = false
        }

        return result
    }
    const update = async  () => {
        const selectedBuildingTypes = activeBuildingTypes().filter(t => !t.isRental).map(t => t.value).join(",")
        const selectedRentalBuildingTypes = activeBuildingTypes().filter(t => t.isRental).map(t => t.value).join(",")
        const mapBounds = {
            _northEast: {
                lat: 39.987642831840844,
                lng: -75.15343666076662
            },
            _southWest: {
                lat: 39.93501296038254,
                lng: -75.24888038635255
            }
        }

        const startingAddressLatitude = 0
        const startingAddressLongitude = 0
        let condoFilter = getActiveToggleFilterValues("condo")
        let licenseFilter = getActiveToggleFilterValues("rental")
        const ownerOccupiedFilter = getActiveToggleFilterValues("owner")

        const results = await getNeighborhoodsPageInfo(
            mapBounds,
            zipCode(),
            blocksFromAddress(),
            startingAddressLatitude,
            startingAddressLongitude,
            searchType(),
            licenseFilter,
            condoFilter,
            ownerOccupiedFilter,
            numUnitsPerList(),
            numLists(),
            selectedBuildingTypes,
            selectedRentalBuildingTypes
        )

        if (results.status === "error") {
            // this.loading = false;
            // this.errorMessage = "Error During Search";
            return;
        } else {
            // this.errorMessage = "";
        }

        setProperties(results.searched_properties)
        setWalkingLists(results.walk_lists)
        Object.keys(results.walk_lists).forEach(walkListName => {
            console.log(walkListName)
            // this.saveNewCustomPropertyList(walkListName);
            // results.walk_lists[walkListName].forEach(thisProperty => {
            //     this.addToSelectedPropertyList(
            //         walkListName,
            //         thisProperty.parcel_number
            //     );
            // });
        });
        // this.lastUpdated = new Date();
    }

    return (<main class="flex flex-col justify-between gap-1">
        <section class="w-full flex justify-between gap-2 py-2 px-4">
            <div class="flex flex-col gap-1 w-1/4 overflow-auto h-[200px]">
                <h3 class="font-medium text-xl">Search</h3>
                <h4>Searching Properties</h4>
                <div class="hidden">
                    Select a geographic area to find the 100 properties with the most violations in that area. These are properties that have an active rental license and violations are only counted if they occurred after 2018-01-01.

                    Click "Search By: Zip Code" to enter a zip code as the geographic area of focus. Click "Search By: Map Boundary" to select your own geographic area of choice. You can do this either by zooming in on the map, or by clicking one of the shapes on the map legend and drawing a custom geographic area.

                    Once you have selected a geographic area, click "Update Map", which will update the markers on the map to represent the 100 properties with the most violations within that area. The list below the map will also populate with this list.
                </div>
                <h4>Generating Lists</h4>
                <div class="hidden">
                    To generate custom lists, you first have to use the "+ Add List" tab to create a new list. Currently, each new list automatically gets assigned a different color. The system can reliably handle about 5 lists at a time, but this could be increased in the future. After creating a list, you can click on a property marker in the map, it's address will pop up along with a drop-down menu with the populated list names, and a button that says 'Add to List'. By clicking on the address, it will then add that property to your own personal list, which can be subsequently downloaded.

                    You can also bulk add properties to the list by going to that list's tab, using the selector tool on the map legend, drawing a shape on the map, and then clicking the 'Add map bounds to list' button.
                </div>
                <h4>Sharing Lists</h4>
                <div class="hidden">
                    After creating a list, you can share out 2 different types of links. There is a 'Link to read-only version of this List' which will link people directly to what is inside the Tab (a copy of the list and a map of just those selected properties). There is also a 'Link to walking directions' which will open up all of the selected properties in an external Google Maps page.

                    If you are working on a list and are not completed with it, you can copy the URL (which changes whenever a property is added) and that URL should return you to the same list that you were working on.
                </div>
            </div>
            <div class="flex flex-col gap-1 w-1/4">
                <h3  class="font-medium text-xl">List</h3>
                <div class="flex justify-between items-center gap-2">
                    <div class="text-sm">Units per list</div>
                    <input type="text" class="border w-1/3 text-right px-2 py-1 rounded-sm" value={numUnitsPerList()} onChange={(e) => {setNumUnitsPerList(e.target.value)}}/>
                </div>
                <div  class="flex justify-between items-center gap-2">
                    <div class="text-sm">Number of lists</div>
                    <input type="text" class="border w-1/3 text-right px-2 py-1 rounded-sm" value={numLists()} onChange={(e) => {setNumLists(e.target.value)}}/>
                </div>


            </div>
            <div class="flex flex-col gap-1 w-1/4">
                <h3 class="font-medium text-xl">Building Type</h3>
                <div class="flex flex-wrap">
                    <For each={buildingTypes}>{(type) =>
                        <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActiveBuildingType(type.value)}} onClick={toggleActiveBuildingType(type)} >{type.text}</button>
                    }
                    </For>
                </div>
            </div>
            <div class="flex flex-col justify-start gap-2 w-1/4">
                <h3 class="font-medium text-xl">Features</h3>
                <div class="flex flex-wrap">
                    <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActive('rental')}} onClick={toggleActive('rental')} >Rental License</button>
                    <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActive('no-rental')}} onClick={toggleActive('no-rental')} >No Rental License</button>
                    <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActive('condo')}} onClick={toggleActive('condo')} >In Condo</button>
                    <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActive('no-condo')}} onClick={toggleActive('no-condo')} >Not in Condo</button>
                    <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActive('owner')}} onClick={toggleActive('owner')} >Owner Occupied</button>
                    <button class={styles["toggle-button"]} classList={{'w-1/2': true, [active]: isActive('no-owner')}} onClick={toggleActive('no-owner')} >Not Owner Occupied</button>
                </div>
            </div>
        </section>
        <section class="flex items-center border-t border-b px-4">
            <div class="font-medium uppercase px-4 py-2 whitespace-nowrap">Search By</div>
            <div class="flex justify-between py-2 border-l w-full ">
                <div class="flex">
                    <select class="py-2 px-4 mx-2 pr-9 block w-full border-gray-200 rounded-md text-sm w-[200px]" name={searchType()}  onChange={(e) => {  setSearchType(e.target.value)}}>
                        <option value="mapBoundary" >Map</option>
                        <option selected value="address" >Address</option>
                        <option value="zipCode" >Zip Code</option>
                    </select>
                    {/*<div class="flex mr-2">*/}
                    {/*    <button class={styles["search-toggle-button"]} classList={{'w-1/3': true, [active]: isSearchType('mapBoundary')}} onClick={toggleSearchType('mapBoundary')} >Map</button>*/}
                    {/*    <button class={styles["search-toggle-button"]} classList={{'w-1/3': true, [active]: isSearchType('address')}} onClick={toggleSearchType('address')} >Address</button>*/}
                    {/*    <button class={styles["search-toggle-button"]} classList={{'w-1/3': true, 'whitespace-nowrap': true, [active]: isSearchType('zipCode')}} onClick={toggleSearchType('zipCode')} >Zip Code</button>*/}
                    {/*</div>*/}
                    <Show when={isSearchType("address")}>
                        <div class="flex items-center gap-2 grow mr-2">
                            <div class="text-sm text-gray-400">Starting Address</div>
                            <input type="text" class="border w-1/3 p-2 rounded-sm grow" value={startingAddress()} onChange={(e) => {setStartingAddress(e.target.value)}}/>
                        </div>
                        <div class="flex items-center gap-2">
                            <div class="text-sm whitespace-nowrap text-gray-400">Blocks from Address</div>
                            <input type="text" class="border w-full p-2 w-10 text-right" value={blocksFromAddress()} onChange={(e) => {setBlocksFromAddress(e.target.value)}}/>
                        </div>
                    </Show>
                    <Show when={isSearchType("zipCode")}>
                        <div class="flex items-center gap-2">
                            <input type="text" class="border w-full p-2" value={zipCode()} onChange={(e) => {setZipCode(e.target.value)}}/>
                            <div class="text-sm whitespace-nowrap text-gray-400">Zip Code</div>
                        </div>
                    </Show>
                </div>
                <button class="bg-emerald-700 px-4 py-2 text-white rounded-lg mr-4" onclick={update}>Update Map</button>
            </div>

        </section>

        <section class="w-full flex gap-4 h-[600px] px-4">
            <div class="w-1/4">

                <h3 class="text-xl font-medium">Searched Properties</h3>
                <For each={walkingLists()}>{(walkingList) =>
                    <div>L {walkingList.location}</div>
                }
                </For>
            </div>
            <div class="w-3/4">
                <NeighborhoodMap properties={properties()} />
            </div>

        </section>
    </main>)
}


export default Neighborhoods