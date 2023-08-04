import {Component, createMemo, Show} from "solid-js";
import {useLocation} from "@solidjs/router";
import "./header.module.css";
const Header: Component = () => {
    const location = useLocation();
    const isHome = createMemo(() => location.pathname === "/");

return (
    <header class="flex justify-between items-center p-4 text-xs md:text-sm lg:text-base">
        <div class="flex gap-4 items-center">
            <a class="px-4 py-2" href="/">Home</a>
            <a class="px-4 py-2" href="/neighborhoods">Neighborhoods</a>
        </div>
        <Show when={!isHome()}>
            <div class="text-xl text-bold text-emerald-800">Who owns Philly?</div>
        </Show>
        <div class="flex gap-4 items-center">
            <a class="px-4 py-2 bg-emerald-700 rounded-lg text-white font-bold" href="/take-action">Take Action</a>
            <a href="/About">About</a>
        </div>
    </header>)
}

export default Header