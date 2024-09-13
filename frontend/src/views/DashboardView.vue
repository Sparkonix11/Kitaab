<script setup>
import Navbar from '../components/Navbar.vue';
import LibrarianDashboard from '../components/LibrarianDashboard.vue';
import UserDashboard from '@/components/UserDashboard.vue';

import 'vue-pdf-embed/dist/style/index.css'


</script>
<template>
<Navbar/>
  <div v-if="$store.state.isLoggedIn">
    <LibrarianDashboard v-if="$store.state.user.role == 'librarian'" />
    <UserDashboard v-if="$store.state.user.role == 'user'" />
  </div>

</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
div.pdf-container {
  height: 1200px;
  overflow: scroll;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 90%;
  margin: auto;
}
</style>

<script>
</script>
