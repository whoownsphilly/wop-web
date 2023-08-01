import {Component, createEffect, createSignal} from "solid-js";
import {useParams} from "@solidjs/router";
import {getPropertyBasicsPageInfo, getPropertyLatestOwnerDetailsInfo} from "../../services/apiFetcher";
import {Property} from "../../models/property.model";
import PropertyBase from "./PropertyBase";


const PropertySummary: Component = () => {
    const params = useParams();
    const [property, setProperty] = createSignal(new Property())
    const [link, setLink] = createSignal()
    const [violationDate, setViolationDate] = createSignal(new Date(2006, 6, 1))
    createEffect(async () => {
        const result= await getPropertyBasicsPageInfo(params.id, violationDate())
        setProperty(Property.toProperty(result))
        const result2 = await getPropertyLatestOwnerDetailsInfo(params.id, violationDate())
        setLink(result2.street_view_link)
    });

    const getLicenseInspectionsLink = (address: string) => {
        return `https://li.phila.gov/property-history/search?address=${address}`;
    }
    return (
        <PropertyBase>
            <div class="w-full lg:w-1/2 h-100">
                <iframe class="h-[600px] w-full" src={link()}></iframe>
            </div>
            <div class="w-full lg:w-1/2">
                <div class="flex justify-between gap-4">
                    <div class="w-1/2 text-right">
                        (<a href={getLicenseInspectionsLink(property().location)} target="_blank">Link to L&I</a>)
                        Rental License
                    </div>
                    <div class="w-1/2 text-left">{property().hasActiveRentalLicense ? "Active" : "None"} : Expires { new Date(property().rentalLicenseExpiration).toLocaleString('en-us', { year:"numeric", month:"short", day:"numeric"})}</div>
                </div>
                <div class="flex justify-between gap-4">
                    <div class="w-1/2 text-right">Year Built</div>
                    <div class="w-1/2 text-left">{property().yearBuilt}</div>
                </div>
                <div class="flex justify-between gap-4">
                    <div class="w-1/2 text-right">Property Type</div>
                    <div class="w-1/2 text-left">
                        <div class="font-bold">{property().categoryCodeDescription}</div>
                        <div>{ property().buildingCodeDescription }</div>
                    </div>
                </div>
                <div class="flex justify-between gap-4">
                    <div class="w-1/2 text-right">Property Estimate</div>
                    <div class="w-1/2 text-left">{property().latestAssessmentMarketValue}</div>
                </div>
                <div class="mt-8">
                    <h2 class="text-left border-b pl-4">Violations</h2>
                    <div class="flex justify-between gap-4">
                        <div class="w-1/2 text-right">Currently Open Violations</div>
                        <div class="w-1/2 text-left">  { property().nViolationsOpen }</div>
                    </div>
                </div>
                <div class="mt-4">
                    <h2 class="text-left border-b pl-4">Since {new Date(violationDate()).toLocaleString('en-us', { year:"numeric", month:"short", day:"numeric"})}</h2>
                    <div class="flex justify-between gap-4">
                        <div class="w-1/2 text-right">Closed Violations</div>
                        <div class="w-1/2 text-left">{ property().nViolationsClosedSince } </div>
                    </div>
                    <div class="flex justify-between gap-4">
                        <div class="w-1/2 text-right">Complaints to 311</div>
                        <div class="w-1/2 text-left">{ property().nComplaintsSince }</div>
                    </div>
                </div>
            </div>
        </PropertyBase>)
}


export default PropertySummary