import { writable, get } from "svelte/store"
import type { TodoItem } from "$lib/models"
import { authStore } from "$lib/auth.store"
import ky from "ky-universal"

const BASE_URL = "http://127.0.0.1:8000/api/todos/"

const client = ky.create({
  prefixUrl: BASE_URL,
  retry: {
    limit: 5,
    statusCodes: [403, 401]
  },
  hooks: {
    beforeRequest: [
      async (options) => {
        const { activeUser, access_token } = get(authStore)
        if (activeUser && access_token) {
          options.headers.set("Authorization", `Bearer ${access_token}`)
        }
      },
    ],
    beforeRetry: [
      async ({ request, error }) => {
        const { activeUser } = get(authStore)
        const access_token = await authStore.login(activeUser)
        if (access_token) {
          request.headers.set("Authorization", `Bearer ${access_token}`)
        }
      },
    ],
  },
})

const createStore = () => {
  const innerStore = writable<TodoItem[]>([])
  const { set, subscribe, update } = innerStore
  return {
    set,
    subscribe,
    update,

    async loadTodos() {
      const res = await client("")
      const items = await res.json<TodoItem[]>()
      set(items)
    },

    async createTodo(newTodo: TodoItem) {
      const res = await client.post("", {
        json: newTodo,
      })
      const item = await res.json<TodoItem>()
      update((items) => [...items, item])
    },

    async updateTodo(id: string, updatedTodo: Partial<TodoItem>) {
      const res = await client.patch(`${id}`, {
        json: updatedTodo,
      })
      const item = (await res.json()) as TodoItem
      this.update((items) => {
        const updateIndex = items.findIndex((x) => x.id === id)
        return [
          ...items.slice(0, updateIndex),
          item,
          ...items.slice(updateIndex + 1),
        ]
      })
    },

    async deleteTodo(id?: string) {
      await client.delete(`${id}`, {
        method: "DELETE",
      })

      update((items) => {
        const index = items.findIndex((x) => x.id === id)
        return [...items.slice(0, index), ...items.slice(index + 1)]
      })
    },

    async toggleComplete(id?: string) {
      if (!id) {
        return
      }
      const items = get(innerStore)
      const index = items.findIndex((x) => x.id === id)
      const item = items[index]
      if (!item) {
        return
      }
      const res = await client.patch(`${id}`, {
        json: {
          completed: !item.completed,
        },
      })
      const updatedItem = await res.json<TodoItem>()
      update((items) => [
        ...items.slice(0, index),
        updatedItem,
        ...items.slice(index + 1),
      ])
    },
  }
}

export const todoStore = createStore()
