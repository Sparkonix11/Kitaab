<script setup>
import '../assets/form.css'
import { editProfile } from '@/services/operations/userProfileAPI';
import { store } from '@/main';
</script>

<template>
    <div class="popup-window">
        <div class="contain">
            <button class="close-button" @click="close">X</button>
            <h1>Edit User Profile</h1>
            <form @submit.prevent="handleSubmit" ref="editUserProfileForm">
            <input
                type="text"
                v-model="editProfileData.username"
                id="edit_username"
                placeholder="Enter your Username"
                name="username"
            />
            <input type="text" v-model="editProfileData.name" id="edit_name" placeholder="Enter your Name" name="name" />
            <input type="email" v-model="editProfileData.email" id="edit_email" placeholder="Enter your Email" name="email" />

            <input
                type="password"
                v-model="editProfileData.password"
                id="edit_password"
                placeholder="Confirm your Password"
                name="password"
            />

            <label for="edit_profile_image" class="upload-label">Change your DP</label><br />
            <input
                class="upload-input"
                type="file"
                v-on:change="handleFileUpload"
                accept="image/*"
                id="edit_profile_image"
                name="edit_profile_image"
            />
            <br /><br />

            <div class="button-group">
                <button type="submit">Submit Changes</button>
            </div>
            </form>
            <p v-if="error" style="color: red">{{ error }}</p>
            <p v-if="resposeMessage" style="color: green">{{ resposeMessage }}</p>
        </div>
    </div>
</template>

<style scoped>
.popup-window {
    position: fixed;
    width: 70%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0.9);
    background-color: white;
    padding: 40px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 999;
}

h1 {
    text-align: center;
}

.close-button {
    position: absolute;
    top: 30px;
    right: 20px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: #999;
}
</style>


<script>
export default {
  data() {
    return {
        editProfileData: {
            username: '',
            name: '',
            email: '',
            password: '',
            image: null
        }
    }
  },
  mounted() {
        this.editProfileData.username = store.state.user.username;
        this.editProfileData.name = store.state.user.name;
        this.editProfileData.email = store.state.user.email;
  },
  methods: {
    
    handleFileUpload(event) {
      this.editProfileData.image = event.target.files[0]
    },
    close() {
            this.$emit('close');
        },
    async handleSubmit() {
      try {
        const formData = new FormData(this.$refs.editUserProfileForm)
        if(this.editProfileData.image){
            formData.append('image', this.editProfileData.image) 
        }
        const { success, message, user } = await editProfile(formData)
        console.log(user)
        if (success) {
          this.responseMessage = message
          this.close()
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
