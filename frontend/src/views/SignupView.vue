<script setup>
import SignupForm from '@/components/SignupForm.vue'
</script>

<template>
  <main>
    <div class="container">
      <SignupForm />
    </div>
  </main>
</template>

<style scoped>
.container {
  width: 60%;
}
main {
  background-image: url(../assets/Background.jpg);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
