import {ApiFetcher} from "../../../services/apiFetcher";
import {Property} from "../../../models/property.model";

export async function load({fetch, params }) {
    const fetcher = new ApiFetcher(fetch)
    const response = await fetcher.getPropertyBasicsPageInfo(params.id)
    console.log(response)
    // const result = await response.json()
    //console.log(result)
    return {
        id: params.id,
       // property: Property.toProperty(result),
    }
}