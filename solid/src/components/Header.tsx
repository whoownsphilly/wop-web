import {Component} from "solid-js";

const Header: Component = () => {
return (
    <header class="flex justify-between p-4 text-xs md:text-sm lg:text-base">
        <div class="flex gap-4 items-center">
            <a class="px-4 py-2" href="/">Home</a>
            <a class="px-4 py-2" href="/neighborhoods">Neighborhoods</a>
        </div>
        <div class="flex gap-4 items-center">
            <a class="px-4 py-2 bg-emerald-700 rounded-lg text-white font-bold" href="/take-action">Take Action</a>
            <a href="/About">About</a>
        </div>
    </header>)
}

export default Header