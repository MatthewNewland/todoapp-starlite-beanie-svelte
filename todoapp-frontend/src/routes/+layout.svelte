<script lang="ts">
  import "./app.css"
  import { browser } from "$app/environment";
  import { authStore } from "$lib/auth.store"
  import { goto } from "$app/navigation"

  if (browser) {
    if ($authStore.activeUser === null) goto("/login")
  }
</script>

<main class="w-1/3 mx-auto mt-7">
  <slot />
</main>