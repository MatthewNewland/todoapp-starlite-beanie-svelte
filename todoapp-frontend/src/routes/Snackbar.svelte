<script lang="ts">
  import { snackbarService } from "$lib/store/snackbar"
</script>

{#if $snackbarService.error || $snackbarService.info || $snackbarService.warning}
  <div
    class="absolute shadow-lg mx-auto w-1/3 px-3 py-3 bottom-12 bg-sky-700 left-0 right-0 flex justify-between"
    class:bg-red-700={$snackbarService.error}
    class:bg-orange-700={$snackbarService.warning}
    class:dark:bg-sky-700={$snackbarService.info}
  >
    <span>{$snackbarService.message}</span>
    <button
      class="material-icons"
      on:click={snackbarService.clear}
    >
      close
    </button>
  </div>
{/if}
