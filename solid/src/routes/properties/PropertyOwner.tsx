import {Component, createEffect, createSignal, Show} from "solid-js";
import PropertyBase from "./PropertyBase";
import {
    getOwnerPageInfoByMailingAddress, getOwnerPageInfoByName,
} from "../../services/apiFetcher";
import {useParams} from "@solidjs/router";
import {CurrencyFormatter} from "../../services/utility.helper";
import PropertyOwnerMap from "./components/PropertyOwnerMap";

const PropertyOwner: Component = () => {

    const params = useParams()
    const [mailingAddressInfo, setMailingAddressInfo] = createSignal({})
   // const [ownerInfo, setOwnerInfo] = createSignal({})

    const [violationDate] = createSignal(new Date(2006, 6, 1))
    const [properties, setProperties] = createSignal([])
    const [propertySummary, setPropertySummary ] = createSignal(0)
    createEffect(async () => {
        const [mailingResults, ownerResults] = await Promise.all([
            getOwnerPageInfoByMailingAddress(params.id, violationDate()),
            getOwnerPageInfoByName(params.id, violationDate())])

        const mailingInfo = {
                    mailingAddress: mailingResults["metadata"]["mailing_address"],
                    mailingAddressBasedNames: mailingResults["results"]["alias_names"],
                    mailingAddressBasedMailingCareOfNames:  mailingResults["results"]["mailing_care_of_names"],
                    mailingAddressBasedPropertyTimelineData: mailingResults["results"]["timeline"],
                    mailingAddressBasedViolations: mailingResults["results"]["violations"],
                    mailingAddressBasedComplaints: mailingResults["results"]["complaints"],
                    mailingAddressBasedOwnerPropertyCountsByName: mailingResults["display_inputs"]["owner_property_counts_by_name"],
                }
        setMailingAddressInfo(mailingInfo)
        const ownerInfo = {
                ownerBasedPropertyTimelineData: ownerResults["results"]["timeline"],
                ownerBasedViolations: ownerResults["results"]["violations"],
                ownerBasedComplaints: ownerResults["results"]["complaints"],
                ownerBasedNames: ownerResults["results"]["alias_names"],
                ownerBasedOwnerPropertyCountsByName: ownerResults["display_inputs"]["owner_property_counts_by_name"],
            }

        const allProperties = ownerInfo.ownerBasedPropertyTimelineData.concat(mailingInfo.mailingAddressBasedPropertyTimelineData)
        const propertySummary = { value: 0, complaints: 0, open: 0, closed: 0 }
        let allUniqueCurrentProperties = []
        let allUniquePropertyParcelNumbers = [];
        allProperties.forEach((property) => {
            if (
                !allUniquePropertyParcelNumbers.includes(
                    property.opa_account_num
                )
            ) {
                allUniquePropertyParcelNumbers.push(property.opa_account_num);
                propertySummary.open += property.n_violations_open;
                propertySummary.closed += property.n_violations_closed;
                propertySummary.complaints += property.n_complaints;
                propertySummary.value += property.market_value;
                if (property.current_owner === true) {
                    allUniqueCurrentProperties.push(property);
                }
            }
        })
        setProperties(allUniqueCurrentProperties)
        setPropertySummary(propertySummary)
    })

    return (<PropertyBase>
        <section class="flex flex-col w-full">
        <div class="flex flex-col flex-col-reverse w-full lg:flex-row gap-4">
            <div class="w-full lg:w-1/2 h-[50vh]">
                <PropertyOwnerMap properties={properties()} />
            </div>
            <div class="w-full lg:w-1/2">
                <div>
                    <div>Mailing Address</div>
                    <span class="text-sm lg:text-xl"> {mailingAddressInfo().mailingAddress}</span>
                </div>
                <Show when={mailingAddressInfo().mailingAddressBasedMailingCareOfNames}>
                    <div class="text-sm lg:text-base">
                        <div class="border-t pt-2">Mailing Care Of</div>
                        <span> {mailingAddressInfo().mailingAddressBasedMailingCareOfNames.join(", ")}</span>
                    </div>
                </Show>
                <div class="flex flex-col w-full border border-black divide-emerald-800">
                    <div class="bg-neutral-300 text-center">Properties currently associated with owner</div>
                    <div class="flex w-full">
                        <div class="w-1/2 bg-neutral-300 px-2 text-center">Properties</div>
                        <div class="w-1/2 bg-neutral-300 px-2 text-center">Total Value</div>
                    </div>
                    <div class="border-t border-black divide-x divide-black flex">
                        <div class="w-1/2 text-center p-2 text-xl">{ properties().length } </div>
                        <div class="w-1/2 text-center p-2 text-xl">{ CurrencyFormatter.USDollar.format(propertySummary().value) }</div>
                    </div>
                </div>
                <div class="mt-4 flex w-full border border-black">
                    <div class="divide-y divide-black">
                        <div class="bg-neutral-300 px-2 text-center">Open Violations</div>
                        <div class="text-2xl text-center pt-4"> { propertySummary().open }</div>
                    </div>
                    <div class="grow border-l border-black">
                        <div class="bg-neutral-300 text-center">Since {new Date(violationDate()).toLocaleString('en-us', { year:"numeric", month:"short", day:"numeric"})}</div>
                        <div class="flex w-full">
                            <div class="w-1/2 bg-neutral-300 px-2 text-center">Closed Violations</div>
                            <div class="w-1/2 bg-neutral-300 px-2 text-center">Complaints</div>
                        </div>
                        <div class="border-t border-black divide-x divide-black flex">
                            <div class="w-1/2 text-center p-2 text-xl">{ propertySummary().closed } </div>
                            <div class="w-1/2 text-center p-2 text-xl">{ propertySummary().complaints }</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="max-w-6xl">
            <table class="w-6xl">
                <thead>
                <tr>
                    <th>color</th>
                    <th>current_owner</th>
                    <th>document_id</th>
                    <th>lat</th>
                    <th>likely_owner</th>
                    <th>lng</th>
                    <th>location</th>
                    <th>location_unit</th>
                    <th>mailing_address_1</th>
                    <th>mailing_address_2</th>
                    <th>mailing_care_of</th>
                    <th>mailing_city_state</th>
                    <th>mailing_street</th>
                    <th>mailing_zip</th>
                    <th>market_value</th>
                    <th>complaints</th>
                    <th>violations</th>
                    <th>violations_closed</th>
                    <th>violations_open</th>
                    <th>opa_account_num</th>
                    <th>opa_address</th>
                    <th>opa_address_unit</th>
                    <th>property_count</th>
                    <th>sold_to</th>
                    <th>source</th>
                    <th>start_dt</th>
                    <th>unit</th>
                </tr>
                </thead>

            </table>
        </div>
        </section>
    </PropertyBase>)
}

export default PropertyOwner