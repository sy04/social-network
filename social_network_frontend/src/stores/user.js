import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      name: null,
      email: null,
      access: null,
      refresh: null,
      avatar: null
    }
  }),
  actions: {
    initStore() {
      if(localStorage.getItem('user.access')) {
        this.user.access = localStorage.getItem('user.access')
        this.user.refresh = localStorage.getItem('user.refresh')
        this.user.id = localStorage.getItem('user.id')
        this.user.name = localStorage.getItem('user.name')
        this.user.email = localStorage.getItem('user.email')
        this.user.avatar = localStorage.getItem('user.avatar')
        this.user.isAuthenticated = true

        this.refreshToken()
      }
    },
    setToken(data) {
      this.user.access = data.access
      this.user.refresh = data.refresh
      this.user.isAuthenticated = true

      localStorage.setItem('user.access', data.access)
      localStorage.setItem('user.refresh', data.refresh)
    },
    removeToken() {
      this.user.refresh = null
      this.user.access = null
      this.user.isAuthenticated = false
      this.user.id = null
      this.user.name = null
      this.user.email = null
      this.user.avatar = null

      localStorage.setItem('user.refresh', '')
      localStorage.setItem('user.access', '')
      localStorage.setItem('user.id', '')
      localStorage.setItem('user.name', '')
      localStorage.setItem('user.email', '')
      localStorage.setItem('user.avatar', '')
    },
    setUserInfo(user) {
      this.user.id = user.id
      this.user.name = user.name
      this.user.email = user.email
      this.user.avatar = user.avatar

      localStorage.setItem('user.id', this.user.id)
      localStorage.setItem('user.name', this.user.name)
      localStorage.setItem('user.email', this.user.email)
      localStorage.setItem('user.avatar', this.user.avatar)
    },
    refreshToken() {
      axios.post('/api/refresh/', {
        refresh: this.user.refresh
      })
      .then((res) => {
        this.user.access = res.data.access
        localStorage.setItem('user.access', res.data.access)

        axios.defaults.headers.common["Authorization"] = "Bearer " + res.data.access
      })
      .catch((err) => {
        console.log(err)
        this.removeToken()
      })
    }
  }
})