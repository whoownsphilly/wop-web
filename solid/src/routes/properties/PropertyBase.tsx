import {Component, createEffect, createSignal} from "solid-js";
import {useParams} from "@solidjs/router";
import {Property} from "../../models/property.model";
import {getPropertyBasicsPageInfo, getPropertyLatestOwnerDetailsInfo} from "../../services/apiFetcher";


const PropertyBase: Component = (props) => {
    const params = useParams();
    // const [property, setProperty] = createSignal(new Property())
    // const [owner, setOwner] = createSignal({})
    // const date = new Date(2006, 6, 1)
    createEffect(async () => {
        // const result= await getPropertyBasicsPageInfo(params.id, date)
        // setProperty(Property.toProperty(result))
        // const result2 = await getPropertyLatestOwnerDetailsInfo(params.id, date)
        // setOwner(result2)
        // setLink(result2.street_view_link)
    });

    return (
        <main class="w-full">
        {/*<h2 class="text-center text-2xl mb-4">*/}
        {/*    <span class="font-bold">{property().location}</span>*/}
        {/*    <span class="mx-2" >is likely owned by</span>*/}
        {/*    <span class="font-bold">{owner().latest_owner}</span>*/}
        {/*</h2>*/}
        <nav class="flex w-full my-2 gap-4 ml-4">
            <a class="nav-button" href={"/properties/" + params.id }>Summary</a>
            <a class="nav-button" href={"/properties/" + params.id + "/timeline" }>Timeline</a>
            <a class="nav-button" href={"/properties/" + params.id + "/owner"}>Owner</a>
        </nav>
            <section class="border-t rounded-sm p-4 flex justify-between gap-4">
            {props.children}
            </section>
    </main>)
}

export default PropertyBase