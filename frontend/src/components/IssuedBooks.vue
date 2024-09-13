<script setup>
import { fetchAllIssuedBooks, returnBook, readBook } from '@/services/operations/bookIssuanceAPI';
import { store } from '@/main';
import VuePdfEmbed from 'vue-pdf-embed'
import 'vue-pdf-embed/dist/style/index.css'
</script>

<template>
    <div>
        <div class="container">
        <h1>Books Issued</h1>
        <div class="book-cards" v-if="issuedBooks.length > 0">
            <div v-for="book in issuedBooks" :key="book.id">
                <div class="card">
                    <img :src=store.state.allBookCovers[book.book_id-1] alt="Book Cover">
                    <div class="card-overlay"></div>
                    <div class="card-overlay-hover"></div>
                    <div class="card-hover-content">
                        <!-- <p>Issued Date - {{ book.book_file_path }}</p> -->
                        <button class="button" v-on:click="readBookHandler(book.book_file_path, book.book_id)">Read Book</button>
                        <button class="button" v-on:click="returndBookHandler(book.book_id)">Return Book</button>
                    </div>
                    <h3>{{ book.book_title }}</h3>by
                    <h4>Return Date - {{ book.return_date }}</h4>
                </div>
            </div>
        </div>
        <p v-else>No Books in this Section.</p>
        </div>
    </div>
    <div class="read-book-container" v-if="showReadBook" @close="closeReadBook">
        <button class="close-button" @click="closeReadBook">X</button>
        <VuePdfEmbed :source=readBookPath />
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
  .close-button {
    position: sticky;
    top: 30px;
    right: 10px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: #999;
    z-index: 999;
}
div.read-book-container{
    position: fixed;
    width: 100%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 40px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 998;
    margin: auto;
    height:100vh;
    overflow-x: hidden;
    overflow-y: scroll;
}
div.container{
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
      font-size: small;
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
        return{
            showReadBook: false,
            issuedBooks: [],
            readBookPath: '',
        }
    },
    mounted() {
        this.fetchIssuedBooks();
    },
    methods: {
        async fetchIssuedBooks(){
            try {
                const { success, responseData } = await fetchAllIssuedBooks();
                if (success) {
                    this.issuedBooks = responseData;
                } else {
                    console.error('Failed to fetch books');
                }
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        },
        async readBookHandler(file_path, bookId){
            try {
                const { success, responseData } = await readBook(bookId);
                console.log(responseData)
                if (success) {
                    let file_path_temp = `../assets${file_path}`           
                    this.readBookPath = new URL(file_path_temp, import.meta.url).href;
                    this.showReadBook = true;
                    this.fetchIssuedBooks();
                } else {
                console.error('Failed to return books');
                }
            } catch (error) {
                console.error('Error returning books:', error);
            }
            
        },
        async returndBookHandler(bookId){
            try {
                const { success, responseData } = await returnBook(bookId);
                console.log(responseData)
                if (success) {
                    this.fetchIssuedBooks();
                } else {
                    console.error('Failed to return books');
                }
            } catch (error) {
                console.error('Error returning books:', error);
            }
        },
        closeReadBook(){
            this.showReadBook = false;
        }
    }
}
</script>