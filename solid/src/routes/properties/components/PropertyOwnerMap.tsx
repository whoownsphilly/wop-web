import {Component, createEffect, mergeProps} from "solid-js";
import "mapbox-gl/dist/mapbox-gl.css"
import mapboxgl from "mapbox-gl";
const PropertyOwnerMap: Component = (props) => {
    props = mergeProps({}, props);

    createEffect( () =>{
        const lngLats = props.properties.map(p => {
            return [p.lng, p.lat]
        })
        mapboxgl.accessToken = "pk.eyJ1Ijoib3Jhbmdlbm90b3JhbmdlIiwiYSI6ImNsbDB4YWlldDF6ODUzZ3BycjM3eHlnbTUifQ.HciS95bDZaZlOb-pncOA1w";
        const map = new mapboxgl.Map({
            container: "map", // container ID
            style: "mapbox://styles/mapbox/dark-v10", // style URL
            center: [-75.165222, 39.952583], // starting position [lng, lat]
            zoom: 12 // starting zoom
        })
        map.on("load", () => {
            console.log(lngLats)
            if(lngLats.length > 0) {
                map.addSource("properties", {
                    type: "geojson",
                    data:  {
                        type: "Feature",
                        geometry: {
                            type: "LineString",
                            coordinates: lngLats
                        },
                    },
                });
                map.addLayer({
                    id: "unclustered-point",
                    type: "circle",
                    source: "properties",
                    paint: {
                        "circle-color": "#047857",
                        "circle-radius": 4,
                        "circle-stroke-width": 1,
                        "circle-stroke-color": "#000000"
                    }
                });

                console.log(map)
            }

        })

    })

    return(<div id="map" class="w-full h-full"></div>)
}

export default PropertyOwnerMap