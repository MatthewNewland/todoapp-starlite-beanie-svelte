import { writable } from "svelte/store"

interface SnackbarStore {
  warning: boolean
  error: boolean
  info: boolean
  message: string
  timeouts: any[]
}

const createService = () => {
  const TIMEOUT_MS = 5000
  const defaultValue: SnackbarStore = {
    warning: false,
    error: false,
    info: false,
    message: "",
    timeouts: []
  }
  const { set, subscribe, update } = writable(defaultValue)

  return {
    set,
    subscribe,
    update,

    showError(message: string) {
      const timeout = setTimeout(() => {
        update((value) => ({ ...value, error: false, message: "" }))
      }, TIMEOUT_MS)
      update((value) => ({ ...value, error: true, message, timeouts: [...value.timeouts, timeout] }))
    },

    showWarning(message: string) {
      const timeout = setTimeout(() => {
        update((value) => ({ ...value, warning: false, message: "" }))
      }, TIMEOUT_MS)
      update((value) => ({ ...value, warning: true, message, timeouts: [...value.timeouts, timeout] }))
    },

    showInfo(message: string) {
      const timeout = setTimeout(() => {
        update((value) => ({ ...value, info: false, message: "" }))
      }, TIMEOUT_MS)
      update((value) => ({ ...value, info: true, message, timeouts: [...value.timeouts, timeout] }))
    },

    clear() {
      subscribe((value) => {
        for (let timeout of value.timeouts) {
          clearTimeout(timeout)
        }
      })
      set(defaultValue)
    }
  }
}

export const snackbarService = createService()
