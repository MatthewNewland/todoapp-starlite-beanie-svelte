<script lang="ts">
  import { snackbarService } from "$lib/store/snackbar"
  import { fly } from "svelte/transition"
  import { flip } from "svelte/animate"
</script>

<div
  class="flex flex-col-reverse gap-3 absolute w-1/3 h-1/2 z-10 left-1/3 right-1/3 bottom-5"
>
  {#each $snackbarService.messages as snackbarMessage (snackbarMessage.id)}
    <div
      transition:fly
      animate:flip
      class="shadow-lg px-3 py-3 bg-sky-700 flex justify-between rounded-md"
      class:bg-red-700={snackbarMessage.error}
      class:bg-orange-700={snackbarMessage.warning}
      class:dark:bg-sky-700={snackbarMessage.info}
    >
      <span>{snackbarMessage.message}</span>
      <button
        class="material-icons"
        on:click={() => snackbarService.clear(snackbarMessage.id)}
      >
        close
      </button>
    </div>
  {/each}
</div>
