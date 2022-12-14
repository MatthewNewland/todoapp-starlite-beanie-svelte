<script lang="ts">
  import "./app.css"
  import { browser } from "$app/environment";
  import { authStore } from "$lib/auth.store"
  import { goto } from "$app/navigation"

  if (browser) {
    if ($authStore.activeUser === null) goto("/login")
  }
</script>

<header class="m-3 w-full flex flex-row">
  <div></div>
  <button
    class="dark:bg-blue-700 px-2 py-1 ml-auto mr-7"
    on:click={authStore.logout}
  >
    Logout
  </button>
</header>
<main class="w-1/3 mx-auto mt-7">
  <slot />
</main>