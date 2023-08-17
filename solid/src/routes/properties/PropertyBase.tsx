import {Component} from "solid-js";
import {useLocation, useParams} from "@solidjs/router";
import styles, { active } from "./propertyBase.module.css"

const PropertyBase: Component = (props) => {
    const params = useParams();
    const location = useLocation()

    const isActive = (route: string) => {
        return location.pathname.endsWith(route)
    }

    return (
        <main class="w-full mt-4">
            <nav class="flex w-full my-2 gap-4 ml-4">
                <a class={styles["nav-button"]} classList={{ [active]: isActive("/" + params.id) }} href={"/properties/" + params.id }>Summary</a>
                <a class={styles["nav-button"]} classList={{ [active]: isActive("/timeline") }} href={"/properties/" + params.id + "/timeline" }>Timeline</a>
                <a class={styles["nav-button"]} classList={{ [active]: isActive("/owner") }} href={"/properties/" + params.id + "/owner"}>Owner</a>
            </nav>
            <section class="border-t rounded-sm p-4">
            {props.children}
            </section>
    </main>)
}

export default PropertyBase