<script setup>
import '../assets/form.css'
import { signup } from '@/services/operations/authAPI';
</script>

<template>
  <div class="contain">
    <h1>Signup</h1>
    <form @submit.prevent="handleSignup" ref="signupForm">
      <input
        type="text"
        v-model="username"
        id="username"
        placeholder="Enter your Username"
        name="username"
      />
      <input type="text" v-model="name" id="name" placeholder="Enter your Name" name="name" />
      <input type="email" v-model="email" id="email" placeholder="Enter your Email" name="email" />

      <input
        type="password"
        v-model="password"
        id="password"
        placeholder="Enter your Password"
        name="password"
      />
      <input
        type="password"
        v-model="confirm_password"
        id="confirm_password"
        placeholder="Confirm your Password"
        name="confirm_password"
      />
      <label for="image" class="upload-label">Upload your DP</label><br />
      <input
        class="upload-input"
        type="file"
        v-on:change="handleFileUpload"
        accept="image/*"
        id="image"
        name="image"
      />
      <br /><br />

      <div class="button-group">
        <button type="submit">Sign up</button>
        <router-link :to="{ name: 'Login' }" class="button"> Login</router-link>
      </div>
    </form>
    <p v-if="error" style="color: red">{{ error }}</p>
    <p v-if="resposeMessage" style="color: green">{{ resposeMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      name: '',
      email: '',
      password: '',
      confirm_password: '',
      image: null
    }
  },
  methods: {
    handleFileUpload(event) {
      this.image = event.target.files[0]
    },
    async handleSignup() {
      try {
        const formData = new FormData(this.$refs.signupForm)
        formData.append('image', this.image) 

        const { success, message, user } = await signup(formData)
        console.log(user)
        if (success) {
          this.responseMessage = message
        } else {
          this.error = message
        }
      } catch (error) {
        console.error('Error:', error)
        this.responseMessage = '' 
        this.error = error.response.data.message
      }
    }
  }
}
</script>
