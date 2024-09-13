<script setup>
 import { store } from '@/main';
 import { editSection } from '@/services/operations/sectionAPI';
</script>

<template>
    <div class="popup-window">
        <button class="close-button" @click="close">X</button>
        <h1>Edit a Section</h1><br>      
        <form @submit.prevent="editSectionHandler" ref="editSectionForm">
            <label for="title">Name:</label><br>
            <input type="text" id="name" name="name" v-model="editSectionData.name" required><br>

            <label for="lyrics">Description:</label><br>
            <textarea id="lyrics" name="description" rows="4" cols="50" v-model="editSectionData.description" required></textarea><br>


            <input type="submit" class='submit-button' value="Edit Section">
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
        width: 100%;
        transition: background-color 0.3s ease;
        text-align: center; 
        text-decoration: none; 
        font-size: small;
    }
    .popup-window {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 100px;
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
    top: 5px;
    right: 5px;
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
        sectionId: Number,
    },
    data(){
        return{
            editSectionData: {
                    name: '',
                    description: ''
                }
        }
    },
    mounted(){
        this.editSectionData.name = store.state.allSections[ this.sectionId - 1].name,
        this.editSectionData.description = store.state.allSections[this.sectionId - 1].description
    },
    methods: {
        close() {
                this.$emit('close');
            },
        async editSectionHandler(){
                const data = {"name": this.editSectionData.name, "description": this.editSectionData.description}
                const sectionId = this.sectionId
                const {success, responseData} = await editSection(data, sectionId)
                if (success) {
                    this.$emit('sectionUpdated', responseData); // Emit event with updated section
                }
        },
            
    }
}
</script>