import { writable } from "svelte/store"

export interface SnackbarStoreMessage {
  warning: boolean
  error: boolean
  info: boolean
  message: string
  id?: number
}

let msgID = 0

const createService = () => {
  const TIMEOUT_MS = 8000
  const defaultStoreMessage: SnackbarStoreMessage = {
    error: false,
    warning: false,
    info: false,
    message: "",
  }
  const { set, subscribe, update } = writable<{
    messages: SnackbarStoreMessage[]
  }>({ messages: [] })

  return {
    set,
    subscribe,
    update,

    show(item: Partial<SnackbarStoreMessage>) {
      let id = msgID++
      setTimeout(() => this.clear(id), TIMEOUT_MS)
      const itemToAdd: SnackbarStoreMessage = {
        ...defaultStoreMessage,
        ...item,
        id,
      }
      update((value) => ({
        ...value,
        messages: [...value.messages, itemToAdd],
      }))
    },

    showError(message: string) {
      this.show({ message, error: true })
    },

    showWarning(message: string) {
      this.show({ message, warning: true })
    },

    showInfo(message: string) {
      this.show({ message, info: true })
    },

    clear(id?: number) {
      if (id === undefined) {
        set({ messages: [] })
        return
      }
      update((value) => {
        const index = value.messages.findIndex((x) => x.id === id)
        if (index < 0) return value
        return {
          ...value,
          messages: [
            ...value.messages.slice(0, index),
            ...value.messages.slice(index + 1),
          ],
        }
      })
    },
  }
}

export const snackbarService = createService()
