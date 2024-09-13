// @vite-ignore

<script setup>
import { fetchDashboardData } from '@/services/operations/librarianAPI';
import chart_1 from '../assets/static/charts/BooksperSections.png'
import chart_2 from '../assets/static/charts/IssuedBooksOverTime.png'

</script>

<template>
    <div class="container">
      <h1>Useful Data</h1>
      <div class="stat">
        <h2>Total Issued Books: {{ fetchedDashboardData.total_issued_books }}</h2>
        <h2>Total Sections: {{ fetchedDashboardData.total_sections }}</h2>
        <h2>Total Books: {{ fetchedDashboardData.total_books }}</h2>
      </div>
      <div class="charts">
        <img :src="chart_1" alt="">
        <img :src="chart_2" alt="">
      </div>
    </div>
</template>

<style scoped>
img {
  width: 600px;
}
div.stat, div.charts {
  display: flex;
  align-items: baseline;
  justify-content: space-evenly;
  width: 100%;
}
div.container{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    justify-content: space-evenly;
    padding:50px 30px ;
    background-color: #f9f9f9;
    width: 95%;
    margin: auto;
    margin-top: 60px;
    border-radius: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    margin-bottom: 60px;
  }
</style>

<script>
export default {
    data(){
      return {
        fetchedDashboardData: []
      }
        
    },
    mounted() {
        this.fetchDashboardDataHandler();
    },
    methods: {
        async fetchDashboardDataHandler(){
          try {
                const { success, responseData } = await fetchDashboardData();
                if (success) {
                  this.fetchedDashboardData = responseData
                } else {
                    console.error('Failed to fetch Dashboard Data');
                }
              } catch (error) {
                    console.error('Error fetching Dashboard Data:', error);
              }
        },
    }
}
</script>