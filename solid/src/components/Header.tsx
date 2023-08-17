import {Component, createMemo, Show} from "solid-js";
import {useLocation} from "@solidjs/router";
import "./header.module.css";
const Header: Component = () => {
    const location = useLocation();
    const isHome = createMemo(() => location.pathname === "/");

return (
    <header>
        <Show when={!isHome()}>
            <div class="text-center text-bold text-emerald-800 mt-2 lg:hidden">Who owns Philly?</div>
        </Show>
        <div class="flex justify-between items-center px-4 py-2 text-xs md:text-sm lg:text-base">
            <div class="flex gap-4 items-center">
                <a class="px-4 py-2" href="/">Home</a>
                <a class="px-4 py-2" href="/neighborhoods">Neighborhoods</a>
            </div>
            <Show when={!isHome()}>
                <div class="text-2xl text-bold text-emerald-800 hidden lg:block">Who owns Philly?</div>
            </Show>
            <div class="flex gap-4 items-center">
                <a class="px-4 py-2 bg-emerald-700 rounded-lg text-white font-bold" href="/take-action">Take Action</a>
                <a href="/About">About</a>
            </div>
        </div>

    </header>)
}

export default Header