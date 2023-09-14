import {Component, createSignal, For, Show} from "solid-js";
import axios from "axios";
import {useNavigate} from "@solidjs/router";
// let searchInput; // use with bind:this to focus element


const domain = "http://localhost:8000/"

const AddressSearch: Component = () => {
    const navigate = useNavigate();
    const [filteredItems, setFilteredItems] = createSignal([]);
    const filterItems = async (event) => {
        const inputValue = event.target.value
        if (event.target.value && inputValue.length > 3) {
            const endpoint = `${domain}api/v1/autocomplete?startswith_str=${inputValue.toLowerCase()}`
            console.log(endpoint)
            const result = await axios.get(endpoint)
            setFilteredItems(result.data.results)
        }
    }

    const selectItem = (item) => {

        let propertyId = item["opa_account_num"];
        console.log(propertyId)
        navigate(`/properties/${propertyId}`, { replace: true })
    }
    return (
        <>
            <input class="py-4 px-8 w-full rounded-full border text-xl hover:shadow-md focus:shadow-md focus:outline-none"
                   type="text"
                   onInput={filterItems}
                   placeholder="Search address or owner..."/>
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