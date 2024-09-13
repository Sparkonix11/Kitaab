<script setup>
import AllSection from './AllSection.vue';
import AZBooks from './AZBooks.vue';
import SectionWiseBooks from './SectionWiseBooks.vue';
import PendingIssuances from './PendingIssuances.vue';
import AllIssuedBooks from './AllIssuedBooks.vue';
import DashboardData from './DashboardData.vue';
</script>

<template>
  <div>
    <DashboardData />    
    
    <PendingIssuances />
    
    <AllIssuedBooks />

    <AllSection />

    <AZBooks />

    <SectionWiseBooks/>
  </div>
</template>

<style scoped>
  
</style>

<script>
export default {
  data(){
    return {
    }
  },
  mounted(){
  },
  methods:{
    
  }
};
</script>