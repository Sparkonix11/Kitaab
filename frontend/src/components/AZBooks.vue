<script setup>
import AddBook from './AddBook.vue';
import EditBook from './EditBook.vue';
import { store } from '@/main';
import { deleteBook, fetchAllBooks } from '@/services/operations/bookAPI';
import { requestBook } from '@/services/operations/bookIssuanceAPI';


</script>

<template>
    <div class="books-container">
      <h1>A - Z Books</h1>
      <div class="book-cards" v-if="store.state.allBooks.length > 0">
        <div v-for="book in sortBooksByTitle" :key="book.id">
          <div class="card">
            <img :src=store.state.allBookCovers[book.id-1] alt="">
            <div class="card-overlay"></div>
            <div class="card-overlay-hover"></div>
            <div class="card-hover-content">
              <button class="button" v-if="store.state.user.role == 'user'" v-on:click="requestBookHandler(book.id)">Request this Book</button>
              <button class="button" v-if="store.state.user.role == 'librarian'" @click="openEditBook(book.id)">Edit</button>
              <button class="button" v-if="store.state.user.role == 'librarian'" @click="deleteBookHandler(book.id)">Delete</button>
            </div>
            <h3>{{ book.title }}</h3>
            <h4>{{ book.author }}</h4>

          </div>
        </div>
      </div>
      <p v-else>No Books found.</p>
      <div><button class="button" v-if="store.state.user.role == 'librarian'" @click="openAddBook">Add Book</button></div>
      <AddBook @bookAdded="bookAdded" v-if="showAddBook" @close="closeAddBook" />
      <EditBook v-if="showEditBook" :bookId="selectedBookId" @close="closeEditBook"   @bookUpdated="onBookUpdated" />
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
h1{
        text-align: center;
    }
div.books-container{
      padding:50px 30px ;
      background-color: #f9f9f9;
      width: 95%;
      margin: auto;
      border-radius: 20px;
      box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
      margin-bottom: 60px;
  }

  div.book-cards{
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    
  }

  div.card{
      display: block;
      position: relative;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      margin: 10px;
      width: 225px;
      height: 300px;
      padding: 0;
      overflow: hidden;
      transition: all  0.3s ease-in-out;
      
  }

  div.card-hover-content {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      color: white;
      opacity: 0;
      transition: all 0.3s ease-in-out;
  }

  div.card-overlay-hover{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.6); 
      border-radius: 8px;
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
  }

  div.card:hover .card-hover-content, div.card:hover div.card-overlay-hover {
      opacity: 1;
      transition: all 0.3s ease-in-out; 
  
  }
  div.card:hover h3, div.card:hover h4{
      opacity: 0;
  }

  div.card h5{
      font-size: 14px;
  }

  div.card:hover img {
      transform: scale(1.1);
      transition: all 0.3s ease-in-out;  
  }

  div.card img{
      width: 100%;
      height: 100%;
      display: block;
      border-radius: 8px 8px 0 0;

  }

  div.card-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5); 
      border-radius: 8px;
  }

  div.card h3{
      position: absolute;
      bottom: 80px;
      left: 0px;
      margin: auto;
      width: 100%;
      font-size: 1.2em;
      text-align: center;
      color: white;
      opacity: 1;
  }

  div.card h4{
      position: absolute;
      bottom: 50px;
      left: 0px;
      margin: auto;
      width: 100%;
      text-align: center;
      font-size: 1em;
      color: white;
      opacity: 1;
  }
</style>

<script>
export default {
    data() {
        return {
            showEditBook: false,
            selectedBookId: null,
            showAddBook: false,
        }
    },
    mounted() {
        this.fetchBooks();

    },
    computed:{
        sortBooksByTitle() {
            return store.state.allBooks.sort((a, b) => a.title.localeCompare(b.title));
        }
    },
    methods: {
        bookAdded(){
            this.fetchBooks();
            this.closeAddBook();
        },    
        openAddBook() {
            this.showAddBook = true;
        },
        closeAddBook() {
            this.showAddBook = false;
        },
        async fetchBooks() {
            try {
                const { success, responseData } = await fetchAllBooks();
                if (success) {
                    console.log(responseData)
                } else {
                    console.error('Failed to fetch books');
                }
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        },

        openEditBook(bookId) {
            this.selectedBookId = bookId;
            this.showEditBook = true;
        },

        closeEditBook() {
            this.showEditBook = false;
        },

        onBookUpdated() {
            this.fetchBooks();
            this.closeEditBook();
        },

        async deleteBookHandler(bookId) {
            try {
                const { success, responseData } = await deleteBook(bookId);
                if (success) {
                    console.log('Book deleted successfully', responseData);
                    this.fetchBooks();
                } else {
                    console.error('Failed to delete book');
                }
            } catch (error) {
                console.error('Error deleting book:', error);
            }
        },
        async requestBookHandler(bookId) {
            const { success, responseData } = await requestBook(bookId)
            console.log(success, responseData)
        },
    }
}
</script>