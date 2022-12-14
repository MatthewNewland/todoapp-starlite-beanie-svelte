import { browser } from "$app/environment"
import { goto } from "$app/navigation"
import { writable, get } from "svelte/store"
import type { User } from "./models"

const BASE_URL = "http://localhost:8000/auth"

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
  const innerStore = writable<UserStore>(loadUser() ?? {
    activeUser: null,
    access_token: "",
    password: ""
  })

  return {
    ...innerStore,

    async login(user: User) {
      if (!user.password && browser) {
        goto("/login")
      }
      const result = await fetch(`${BASE_URL}/token`, {
        method: "POST",
        headers: {
          authorization: `${user.name ?? user.email}:${user.password}`,
        },
      })
      const json = await result.json()
      const { access_token, userOut } = json
      this.set({
        access_token,
        activeUser: { ...userOut, ...user },
        password: user.password
      })
      this.dumpUser()
      return access_token
    },

    dumpUser() {
      let storeCopy = { ...get(authStore) }
      delete storeCopy.password
      storeCopy.activeUser = { ...storeCopy.activeUser }
      delete storeCopy.activeUser.password
      localStorage.setItem("user", JSON.stringify(storeCopy))
    }
  }
}

export const authStore = createStore()
