import {Component} from "solid-js";
import {useParams} from "@solidjs/router";


const PropertySummary: Component = () => {

    const params = useParams();
    return (<main class="w-full p-4 pt-8">
        <h2 class="text-center font-bold text-xl">{params.id} 5942 DELANCEY ST
            IS LIKELY OWNED BY
            PS HOMES 2 LP PREMISES ZZ
        </h2>
        <nav class="flex justify-evenly w-full my-2">
            <a class="nav-button" href={"/properties/" + params.id }>Summary</a>
            <a class="nav-button" href={"/properties/" + params.id + "/details" }>Property Details</a>
            <a class="nav-button" href={"/properties/" + params.id + "/owner"}>Owner Details</a>
            <a class="nav-button" href={"/properties/" + params.id + "/crowd"}>Crowd-Sourced</a>
        </nav>
        <section class="border rounded-sm p-4">
        </section>
    </main>)
}


export default PropertySummary