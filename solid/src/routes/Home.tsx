import {Component} from "solid-js";
import AddressSearch from "../components/AddressSearch";

const Home: Component = () => {
   return (<main class="flex flex-col items-center h-screen pt-36 p-4">
        <h1 class="text-4xl text-bold text-emerald-800">Who Owns Philly?</h1>
        <p class="text-center"> Find out who owns what in Philly, what else
            they might own in the city, and information about their properties.</p>

        <div class="py-8 flex w-full lg:w-1/2 flex-col items-center">
            <AddressSearch/>
            <div class="text-center">
                Enter a <b>Philly address</b>, <b>landlord's name</b>, or <b>property manager</b>.
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
        </div>
    </main>)
}


export default Home