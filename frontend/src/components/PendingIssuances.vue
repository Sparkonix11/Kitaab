<script setup>
import { fetchAllPedningIssuance, issueBook, denyIssue } from '@/services/operations/bookIssuanceAPI';
import { store } from '@/main';
</script>

<template>
    <div class="issuance-container" v-if="store.state.user.role == 'librarian'" >
      <h1>Pending Book Issuance Requests</h1>
        <div v-if="pendingBookRequests.length > 0">
          <ul>
            <li class="issue-request">
              <div><strong>Book</strong> </div>
              <div><strong>Requested By</strong></div>
              <div><strong>User mail</strong></div>
              <div><strong>Action</strong></div>
            </li>
            <div v-for="book in pendingBookRequests" :key="book.id">

              <li class="issue-request">
                <div>{{ book.book_title }}</div>
                <div>{{ book.user_name }}</div>
                <div>{{ book.user_email }}</div>
                <div class="edit-issue-buttons">
                <button class="button" @click="issueBookHandler(book.book_id, book.user_id)">Approve</button>
                <button class="button" @click="denyIssueHandler(book.book_id, book.user_id)">Deny</button>

                </div>
              </li>
            </div>
          </ul>
        </div>
        <p v-else>No Pending Request.</p>
    </div>
</template>

<style scoped>
h1, p{
    text-align: center;
  }
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
 div.issuance-container {
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
  li.issue-request {
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

  li.issue-request > div {
      flex: 1; 
      text-align: center;
      box-sizing: border-box;
  }
  div.edit-issue-buttons > button{
      margin: 7px;  
  }
  div.edit-issue-buttons {
      display: flex;
      align-items: center;
     justify-content: center;
  }
</style>

<script>
    export default {
        data() {
            return {
                pendingBookRequests: [],
            }
        },
        mounted() {
            this.fetchPendingIssuance();

        },
        methods: {
            async fetchPendingIssuance(){
            try {
                const { success, responseData } = await fetchAllPedningIssuance();
                if (success) {
                this.pendingBookRequests = responseData;
                } else {
                console.error('Failed to fetch books');
                }
            } catch (error) {
                console.error('Error fetching books:', error);
            }
            },

            async issueBookHandler(bookId, userId){
                try {
                    const { success, responseData } = await issueBook(bookId, userId);
                    console.log(responseData)
                    if (success) {
                        this.fetchPendingIssuance();
                    } else {
                        console.error('Failed to issue book');
                    }
                } catch (error) {
                    console.error('Error issuing books:', error);
                }
            },
            async denyIssueHandler(bookId, userId){
                try {
                    const { success, responseData } = await denyIssue(bookId, userId);
                    console.log(responseData)
                    if (success) {
                        this.fetchPendingIssuance();
                    } else {
                        console.error('Failed to issue book');
                    }
                } catch (error) {
                    console.error('Error issuing books:', error);
                }
            }
        }
    }
</script>