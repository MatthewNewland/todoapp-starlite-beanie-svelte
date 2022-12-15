import { browser } from "$app/environment"
import { goto } from "$app/navigation"
import { writable, get } from "svelte/store"
import type { User } from "../models"
import ky from "ky-universal"
import { snackbarService } from "./snackbar"

const BASE_URL = "http://localhost:8000/auth"

const client = ky.create({
  prefixUrl: BASE_URL,
})

export type UserStore = any & {
  activeUser: User
  access_token: string
}

const loadUser = (): UserStore => {
  let result = localStorage.getItem("user")
  if (!result) {
    return null
  }
  const initialStoreValue = JSON.parse(result)
  return initialStoreValue
}

const createStore = () => {
  const innerStore = writable<UserStore>(
    loadUser() ?? {
      activeUser: null,
      access_token: "",
      password: "",
    }
  )

  return {
    ...innerStore,

    async login(user: User) {
      if (!user.password && browser) {
        goto("/login")
      }
      const result = await client.post("token", {
        headers: {
          authorization: `${user.name ?? user.email}:${user.password}`,
        },
      })
      if ([401, 403].includes(result.status)) {
        snackbarService.showError("Error: invalid user credentials. Please login again.")
      }
      const json = await result.json<any>()
      const { access_token, userOut } = json
      this.set({
        access_token,
        activeUser: { ...userOut, ...user },
        password: user.password,
      })
      this.dumpUser()
      return access_token
    },

    logout() {
      const unsub = innerStore.subscribe(store => {
        client.post("logout", {
          headers: {
            authorization: `Bearer ${store.access_token}`
          }
        })
      })
      unsub()
      goto("/login")
    },

    dumpUser() {
      let storeCopy = { ...get(authStore) }
      delete storeCopy.password
      storeCopy.activeUser = { ...storeCopy.activeUser }
      delete storeCopy.activeUser.password
      localStorage.setItem("user", JSON.stringify(storeCopy))
    },
  }
}

export const authStore = createStore()
