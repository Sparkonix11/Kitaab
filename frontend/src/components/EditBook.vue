User
<script setup>
import { store } from '@/main';
import { editBook } from '@/services/operations/bookAPI';
</script>

<template>
    <div class="popup-window">
        <button class="close-button" @click="close">X</button>
        <h1>Edit a Book</h1>
        <form @submit.prevent="editBookHandler" ref="editBookForm">
            <label for="title">Title:</label><br>
            <input type="text" id="name" name="title" v-model="editBookData.title" required><br>

            <label for="author">Author:</label><br>
            <input type="text" id="author" name="author" v-model="editBookData.author" required><br>

            <label for="description">Description:</label><br>
            <input type="text" id="description" name="description" v-model="editBookData.description" required><br>

            <label for="section">Section:</label><br>
            <select id="section" name="section" v-model="editBookData.section" required>
                <option v-for="section in sections" :value="section.id" :key="section.id">{{ section.name }}</option>
            </select>

            <label for="editImage" class="upload-label">Cover Image:</label><br>
            <input class="upload-input" type="file" v-on:change="handleEditImageUpload" accept="image/*" id="editImage"
                name="editImage" /><br>
            <input type="submit" class='submit-button' value="Edit Book">
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
    props: {
        bookId: Number,
    },
    data() {
        return {
            sections: [],
            editBookData: {
                title: '',
                author: '',
                description: '',
                image: null,
                section: null,
            }
        }
    },
    mounted() {
            this.editBookData.title = store.state.allBooks[this.bookId - 1].title,
            this.editBookData.author = store.state.allBooks[this.bookId - 1].author,
            this.editBookData.description = store.state.allBooks[this.bookId - 1].description,
            this.editBookData.section = store.state.allBooks[this.bookId - 1].section,
            this.sections = this.$store.state.allSections
    },
    methods: {
        close() {
            this.$emit('close');
        },
        handleEditImageUpload(event) {
            this.editBookData.image = event.target.files[0]
        },
        async editBookHandler() {
            const formData = new FormData(this.$refs.editBookForm);
            formData.append('section', this.editBookData.section)
            if (this.editBookData.image) {
                formData.append('image', this.editBookData.image);
            }
            const bookId = this.bookId
            const { success, responseData } = await editBook(formData, bookId)
            console.log(success, responseData)
            if (success) {
                this.$emit('bookUpdated', responseData); 
            }
        },

    }
}
</script>
