import {Component} from "solid-js";
import AddressSearch from "../components/AddressSearch";

const Home: Component = () => {
   return (<main class="flex flex-col items-center h-screen lg:pt-36 p-4">
        <h1 class="text-4xl text-bold text-emerald-800 mb-2">Who Owns Philly?</h1>
        <p class="text-center"> Find out who owns what in Philly, what else
            they might own in the city, and information about their properties.</p>

        <div class="py-8 flex w-full lg:w-1/2 flex-col items-center">
            <AddressSearch/>
            <div class="text-center mt-2 text-xs lg:text-sm">
                Enter a <b>Philly address</b>, <b>landlord's name</b>, or <b>property manager</b>.
            </div>
            <p class="text-center mt-2 text-xs lg:text-sm">
                <b>Is the address not showing up?</b> Search for the address on
                <a href="https://atlas.phila.gov">atlas.phila.gov</a> to see how the
                City formats addresses and owner names. We try our best to match
                addresses to the City’s format, but sometimes the City formats addresses
                in ways we can't detect.
            </p>

        </div>
       <div class="w-full">
           <div>View sample owner properties</div>
           <div class="w-full flex flex-col lg:flex-row justify-between gap-4">
               <div class="border lg:w-1/3">
                   <div class="p-4 rounded-md flex flex-col justify-between ">
                       <div><a href="/properties/871288650">Odin Properties</a></div>
                       <div class="text-gray-400">1200 Callowhill St Suite 403</div>
                       <div class="mt-2">Odin Properties was founded in 2009 by real estate investor Philip Balderston. Balderston left Tower Investments (Bart Blatstein) after the foreclosure crisis to buy distressed properties in Philadelphia.</div>
                   </div>
                       <div class="text-gray-400 border-t p-2">~470 Properties</div>
                   </div>
               <div class="border lg:w-1/3">
                   <div class="p-4 rounded-md flex flex-col justify-between ">
                       <div class="text-blue-500"><a href="/properties/871288650">Allan Domb Realty</a></div>
                       <div class="text-gray-400">1845 Walnut St Suite 2200</div>
                       <div class="mt-2"> 1845 Walnut is a large office building on Rittenhouse Square with many suites, and several suites are associated with realty companies...</div>
                   </div>
                   <div class="text-gray-400 border-t p-2">~470 Properties</div>
               </div>
               <div class="border lg:w-1/3">
                   <div class="p-4 rounded-md flex flex-col justify-between ">
                       <div><a href="/properties/871288650">Pearl Properties</a></div>
                       <div class="text-gray-400">110 S 19th St Suite 300</div>
                       <div class="mt-2"> Pearl Properties works in real estate development, construction,
                           residential leasing, and property management. Multiple LLCs receive
                           mail to Pearl Properties' office, including 14 WA Partners LP,
                           associated with 1401 Walnut - Pearl Apartments.</div></div>
                   <div class="text-gray-400 border-t p-2">~470 Properties</div>
               </div>
           </div>

       </div>
    </main>)
}


export default Home