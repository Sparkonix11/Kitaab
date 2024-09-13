<script setup>
import { addBook } from '@/services/operations/bookAPI';
</script>
<template>
    <div class="popup-window">
        <button class="close-button" @click="close">X</button>
        <h1>Add a Book</h1>
        <form @submit.prevent="addBookHandler" ref="addBookForm">
            <label for="title">Title:</label><br>
            <input type="text" id="name" name="title" v-model="addBookData.title" required><br>

            <label for="author">Author:</label><br>
            <input type="text" id="author" name="author" v-model="addBookData.author" required><br>

            <label for="description">Description:</label><br>
            <input type="text" id="description" name="description" v-model="addBookData.description" required><br>

            <label for="section">Section:</label><br>
            <select id="section" name="section" v-model="addBookData.section" required>
                <option v-for="section in sections" :value="section.id" :key="section.id">{{ section.name }}</option>
            </select><br><br>

            <label for="image" class="upload-label">Cover Image:</label>
            <input
            class="upload-input"
            type="file"
            v-on:change="handleImageUpload"
            accept="image/*"
            id="image"
            name="image"
        /><br>  

            <label for="book" class="upload-label">Book:</label><br>
            <input
            class="upload-input"
            type="file"
            v-on:change="handleFileUpload"
            accept=".pdf"
            id="book"
            name="book"
        /><br> 

            <input type="submit" class='submit-button' value="Add Book">
        </form>
    </div>
</template>

<style scoped>
    .submit-button {
        box-sizing: border-box; 
        display: block;
        padding: 12px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        color: #ffffff;
        background-color: #ff7357;
        width: 42%;
        transition: background-color 0.3s ease;
        text-align: center; 
        text-decoration: none; 
        font-size: small;
    }
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
    .fade-enter-active,
    .fade-leave-active {
    transition: opacity 0.5s;
    }
    .fade-enter,
    .fade-leave-to {
    opacity: 0;
    }
</style>

<script>
    export default {
        data() {
            return {
                sections:[],
                addBookData: {
                    title: '',
                    author: '',
                    description: '',
                    section: null,
                    image: null,
                    book: null
                }
            }
        },
        mounted() {
            this.sections = this.$store.state.allSections
        },
        methods: {
            close() {
                this.$emit('close');
            },
            handleImageUpload(event) {
                this.addBookData.image = event.target.files[0]
            },
            handleFileUpload(event) {
                this.addBookData.book = event.target.files[0]
            },
            async addBookHandler(){
                const formData = new FormData(this.$refs.addBookForm)
                formData.append('image', this.addBookData.image) 
                formData.append('book', this.addBookData.book)
                formData.append('section', this.addBookData.section)

                // const response = await 
                const {success, responseData} = await addBook(formData)
                console.log(success, responseData)
                if (success) {
                    this.$emit('bookAdded');
                    // Clear the form
                    this.addBookData.title = '';
                    this.addBookData.author = '';
                    this.addBookData.description = '';
                    this.addBookData.section = null
                    this.addBookData.image = null;
                    this.addBookData.book = null;
                }
            }
        }
    }
</script>