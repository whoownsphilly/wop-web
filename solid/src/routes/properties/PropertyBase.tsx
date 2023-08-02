import {Component, createEffect, createSignal} from "solid-js";
import {useParams} from "@solidjs/router";
import {Property} from "../../models/property.model";
import {getPropertyBasicsPageInfo, getPropertyLatestOwnerDetailsInfo} from "../../services/apiFetcher";


const PropertyBase: Component = (props) => {
    const params = useParams();
    return (
        <main class="w-full mt-4">
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