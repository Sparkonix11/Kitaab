<script setup>
import AddSection from './AddSection.vue';
import EditSection from './EditSection.vue';
import { deleteSection, fetchAllSections } from '@/services/operations/sectionAPI';
import { store } from '@/main';

</script>

<template>
        <div class="section-container">
      <h1>All Sections</h1>
      <div v-if="store.state.allSections.length > 0">
        <ul>
          <li class="section">  
              <div><strong>Name</strong></div>
              <div><strong>Description</strong></div>
              <div v-if="store.state.user.role == 'librarian'" class="edit-section-buttons">
                <strong>Actions</strong>
              </div>
              <!-- <div >              
                <strong>
                  Books
                </strong>
              </div> -->
  
            </li>
          <div v-for="section in store.state.allSections" :key="section.id">
            <li class="section">  
              <div>{{ section.name }}</div>
              <div>{{ section.description }}</div>
              <div class="edit-section-buttons" v-if="store.state.user.role == 'librarian'">
                <button class="button2" @click="openEditSection(section.id)">Edit</button>
                <button class="button2" @click="deleteSectionHandler(section.id)">Delete</button>
              </div>
              <!-- <div v-if="section.books.length > 0">              
                <div v-for="book in section.books" :key="book.id">
                  {{ book.title }} {{ book.author }}
                  <button @click="openEditBook(book.id)">Edit</button>
                  <button @click="deleteBookHandler(book.id)">Delete</button>
                </div>
              </div>
              <div v-else>    
                <p>No Books in this Section yet.</p>
              </div>   -->
            </li>
          </div>
        </ul>
      </div>
      <p v-else>No sections found.</p>
      <div v-if="store.state.user.role == 'librarian'" ><button class="button" @click="openAddSection">Add Section</button></div> 
      <AddSection @sectionCreated="sectionCreated" v-if="showAddSection" @close="closeAddSection" />
      <EditSection v-if="showEditSection" :sectionId="selectedSectionId" @close="closeEditSection"   @sectionUpdated="onSectionUpdated" />
    </div>
</template>

<style scoped>
.button{
    box-sizing: border-box;
    display: block;
    padding: 12px 24px;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    color: #ff7357;
    border: solid 2px #ff7357;
    background-color: transparent;
    width: 100%;
    transition: background-color 0.3s ease;
    text-align: center; 
    text-decoration: none; 
    font-size: small;
    margin: 10px auto;
}
.button:hover{
    background-color: #ff7357;
    color: white;
}
.button2{
    box-sizing: border-box; 
    display: block;
    padding: 12px 24px;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    color: #ff7357;
    border: solid 2px #ff7357;
    background-color: transparent;
    transition: background-color 0.3s ease;
    text-align: center; 
    text-decoration: none; 
    font-size: small;
    margin: 10px auto;
}
.button2:hover{
    background-color: #ff7357;
    color: white;
}
h1, p{
    text-align: center;
  }
  div.section-container {
      display: flex;
      flex-direction: column;
      width: 95%;
      background-color: #f9f9f9;
      border-radius: 20px;
      box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
      padding: 30px;
      margin: 60px auto;
  }
  strong{
    font-weight: 600;
  }
  li.section {
      display: flex;
      flex-direction: row;
      justify-content: space-around;
      align-items: center;
      width: 100%;
      margin: 5px 0px;
      background: #ffffff;
      padding: 10px;
      box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
  }

  li.section > div {
      flex: 1; 
      text-align: center;
      box-sizing: border-box;
  }
  div.edit-section-buttons > button{
      margin: 7px;  
  }
  div.edit-section-buttons {
      display: flex;
      align-items: center;
     justify-content: center;
  }
</style>

<script>
export default {
    data() {
        return{
            showEditSection: false,
            selectedSectionId: null,
            showAddSection: false,
        }
    },
    mounted() {
        this.fetchSections();
    },
    methods: {
      sectionCreated(){
          this.fetchSections();
          this.closeAddSection();
      },
      openAddSection() {
          this.showAddSection = true;
      },
      closeAddSection() {
          this.showAddSection = false;
      },
      async fetchSections() {
        try {
          const { success, responseData } = await fetchAllSections();
          if (success) {
            console.log(responseData)
          } else {
            console.error('Failed to fetch sections');
          }
        } catch (error) {
          console.error('Error fetching sections:', error);
        }
      },

      openEditSection(sectionId) {
        this.selectedSectionId = sectionId;
        this.showEditSection = true;
      },

      closeEditSection() {
        this.showEditSection = false;
        this.fetchSections();
      },

      onSectionUpdated() {
        this.closeEditSection();
      },

      async deleteSectionHandler(sectionId) {
        try {
          const { success, responseData } = await deleteSection(sectionId);
          if (success) {
            console.log('Section deleted successfully', responseData);
            this.fetchSections();
          } else {
            console.error('Failed to delete section');
              }
          } catch (error) {
          console.error('Error deleting section:', error);
            }
      },
    },
}
</script>