<script setup>
import LoginForm from '../components/LoginForm.vue';



</script>

<template>
    <main>
        <div class="container">
            <LoginForm/>
        </div>
    </main>
</template>

<style scoped>
    .container {
        width: 60%;
    }
    main{
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