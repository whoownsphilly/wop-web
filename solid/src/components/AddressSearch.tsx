import {Component, createSignal, For, Show} from "solid-js";
import axios from "axios";
import {useNavigate} from "@solidjs/router";
// let searchInput; // use with bind:this to focus element


const domain = "http://localhost:8081/"

const AddressSearch: Component = () => {
    const [filteredItems, setFilteredItems] = createSignal([]);
    const filterItems = async (event) => {
        const inputValue = event.target.value
        if (event.target.value && inputValue.length > 3) {
            const endpoint = `${domain}api/v1/autocomplete?startswith_str=${inputValue.toLowerCase()}`
            const result = await axios.get(endpoint)
            setFilteredItems(result.data.results)
        }
    }

    const selectItem = (item) => {
        const navigate = useNavigate();
        let propertyId = item["opa_account_num"];
        navigate(`/property/${propertyId}`, { replace: true })
    }
    return (
        <>
            <input class="py-4 px-8 w-full rounded-full border text-xl"
                   type="text"
                   onInput={filterItems}
                   placeholder="Search address or owner..."/>
            {filteredItems.length}
        <Show when={filteredItems().length > 0} >
            <ul class="relative mt-2 w-full border divide-y shadow-md rounded-lg">
                <For each={filteredItems()}>
                    {(item) =>
                        <li class="p-2 hover:bg-emerald-200 hover:cursor-pointer" onclick={[selectItem, item]} >
                            {item.computed_location}
                        </li>
                    }
                </For>
            </ul>
        </Show>
        </>)
}

export default AddressSearch