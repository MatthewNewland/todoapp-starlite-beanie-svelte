<script lang="ts">
  import { createEventDispatcher } from "svelte"
  export let value: string
  let editing: boolean

  const handleKeydown = (e: KeyboardEvent) => {
    if (e.key !== "Enter") {
      return
    }
    editing = !editing
    dispatch("blur")
  }

  const dispatch = createEventDispatcher()
</script>

<div class="flex flex-row justify-between flex-grow">
  {#if !editing}
    <span>{value}</span>
  {:else}
    <input
      type="text"
      bind:value
      on:keydown={handleKeydown}
    />
  {/if}
  <button class="material-icons" on:click={() => (editing = !editing)}>
    edit
  </button>
</div>
