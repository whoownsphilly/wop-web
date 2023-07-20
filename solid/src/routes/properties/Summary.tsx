import {Component} from "solid-js";
import {useParams} from "@solidjs/router";


const PropertySummary: Component = () => {

    const params = useParams();
    return (<div>Summary {params.id}</div>)
}


export default PropertySummary