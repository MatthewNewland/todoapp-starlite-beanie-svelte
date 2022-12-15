<script lang="ts">
  import { goto } from "$app/navigation"
  import { page } from "$app/stores"
  import { authStore, type UserStore } from "$lib/store/auth"

  let username = ""
  let password = ""

  const doLogin = async () => {
    await authStore.login({
        name: username,
        password
    })

    const redirect = $page.url.searchParams.get("redirect")
    goto(redirect ?? "/")
  }
</script>

<form
  on:submit|preventDefault={doLogin}
  class="grid gap-2 grid-cols-2 place-items-stretch"
>
  <label for="username">Username/email:</label>
  <input type="text" bind:value={username} />
  <label for="password">Password:</label>
  <input type="password" bind:value={password} />
  <button type="submit" class="col-span-2 dark:bg-sky-700 px-2 py-1">
    Login
  </button>
</form>
