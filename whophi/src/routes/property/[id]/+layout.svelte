<script lang="ts">
    import { page } from '$app/stores';
</script>

<main class="w-full p-4 pt-8">
    <h2 class="text-center font-bold text-xl">{$page.params.id} 5942 DELANCEY ST
        IS LIKELY OWNED BY
        PS HOMES 2 LP PREMISES ZZ
        <!--{$page.data.property}-->
    </h2>
    <nav class="flex justify-evenly w-full my-2">
        <a class="nav-button" href="/property/{$page.params.id}">Summary</a>
        <a class="nav-button" href="/property/{$page.params.id}/details">Property Details</a>
        <a class="nav-button" href="/property/{$page.params.id}/owner">Owner Details</a>
        <a class="nav-button" href="/property/{$page.params.id}/crowd">Crowd-Sourced</a>
    </nav>
    <section class="border rounded-sm p-4">
        <slot />
    </section>
</main>
<style>
    .nav-button {
        @apply px-6 py-2 rounded-lg bg-gray-100 border border-white;
    }

    .nav-button:hover {
        @apply border-gray-300;
    }
</style>