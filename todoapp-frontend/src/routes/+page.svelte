<script lang="ts">
  import { browser } from "$app/environment"
  import { goto } from "$app/navigation"
  import { authStore } from "$lib/auth.store"
  import { onMount } from "svelte"
  import ItemEdit from "./ItemEdit.svelte"
  import { todoStore } from "./todo.store"

  onMount(async () => {
    if (browser && !$authStore.activeUser) {
      goto("/login")
    }
  })

  $: incompleteTasks = $todoStore.filter((item) => !item.completed)
  $: completeTasks = $todoStore.filter((item) => item.completed)
  $: todoStore.loadTodos(), $authStore.access_token

  let nextTask = ""

  const addTask = async () => {
    if (!nextTask) {
      return
    }
    await todoStore.createTodo({
      task: nextTask,
      completed: false,
    })

    nextTask = ""
  }
</script>

<form
  on:submit|preventDefault={addTask}
  class="flex flex-row gap-0 mb-7 w-full"
>
  <input type="text" placeholder="Next task..." bind:value={nextTask} />
  <button
    type="submit"
    class="px-2 py-1 bg-blue-600 text-slate-50 dark:bg-blue-700"
    >Add Task</button
  >
</form>

<h3 class="text-lg font-semibold">Incomplete tasks:</h3>
<ul class="ml-5 list-disc">
  {#each incompleteTasks as item (item.id)}
    <li class="flex flex-row gap-3 justify-between">
      <ItemEdit bind:value={item.task} on:blur={async () => {
        await todoStore.updateTodo(item.id ?? "", item)
      }} />
      <span class="flex flex-row gap-3 place-items-center">
        <input
          type="checkbox"
          checked={item.completed}
          on:change={() => todoStore.toggleComplete(item.id)}
        />
        <button
          class="aspect-square material-icons"
          on:click={() => todoStore.deleteTodo(item.id)}
        >
          delete
        </button>
      </span>
    </li>
  {/each}
</ul>
<h3 class="text-lg font-semibold">Complete tasks:</h3>
<ul class="ml-5 list-disc">
  {#each completeTasks as item (item.id)}
    <li class="flex flex-row justify-between">
      <span class="line-through">{item.task}</span>
      <span class="flex flex-row gap-3 place-items-center">
        <input
          type="checkbox"
          checked={item.completed}
          on:change={() => todoStore.toggleComplete(item.id)}
        />
        <button
          class="aspect-square material-icons"
          on:click={() => todoStore.deleteTodo(item.id)}
        >
          delete
        </button>
      </span>
    </li>
  {/each}
</ul>
