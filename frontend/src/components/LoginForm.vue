<script setup>
import { login } from '@/services/operations/authAPI'
import '../assets/form.css'

</script>

<template>
  <div class="contain">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin" ref="loginForm">
      <input
        type="text"
        v-model="username"
        id="username"
        placeholder="Enter your Username"
        name="username"
      />
      <input
        type="password"
        v-model="password"
        id="password"
        placeholder="Enter your Password"
        name="password"
      />
      <div class="button-group">
        <button type="submit">Login</button>
        <router-link :to="{ name: 'Signup' }" class="button">Sign up </router-link>
      </div>
    </form>
    <p v-if="error" style="color: red">{{ error }}</p>
    <p v-if="responseMessage" style="color: green">{{ responseMessage }}</p>
  </div>
</template>

<script>

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      responseMessage: '',
      user: ''
    }
  },
  methods: {
    async handleLogin() {
      const formData = new FormData(this.$refs.loginForm)
      const { success, message, user } = await login(formData)
      console.log(user)
      if (success) {
        this.responseMessage = message
      } else {
        this.error = message
      }
    }
  }
}
</script>
