import './assets/main.css'

import { createApp } from 'vue'
import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { logout } from './services/operations/authAPI'
import App from './App.vue'
import router from './router'


const store = createStore({
  state() {
    return {
      isLoggedIn: false,
      user: null,
      allSections: [],
      allBooks: [],
      allBookCovers: [],
    }
  },
  mutations: {
    login(state, user) {
      state.isLoggedIn = true
      state.user = user
    },
    logout(state) {
      state.isLoggedIn = false
      state.user = null
    },
    setAllSection(state, allSections) {
      state.allSections = allSections
    },
    setAllBook(state, allBooks){
      state.allBooks = allBooks
    },
    setAllBookCovers(state, allBooksCovers){
      state.allBookCovers = allBooksCovers
    }
  },
  actions: {
    async performLogout({ commit }) {
      try {
        // Call the logout function
        const { success } = await logout()

        if (success) {
          // Update state if logout is successful
          commit('logout')
        } else {
          // Handle logout failure if needed
          console.error('Logout failed.')
        }
      } catch (error) {
        console.error('Error:', error)
      }
    }
  },
  getters: {
    isLoggedIn: (state) => state.isLoggedIn,
    user: (state) => state.user,
    allSections: (state) => state.allSections
  },
  plugins: [
    createPersistedState({
      storage: window.localStorage // Use local storage for persistence
      // Alternatively, you can use sessionStorage:
      // storage: window.sessionStorage
    })
  ]
})
const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')

export { store }
