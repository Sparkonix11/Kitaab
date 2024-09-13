<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import SearchResult from './SearchResult.vue';
import EditProfile from './EditProfile.vue';
import logo from '../assets/logo.jpeg'
import { store } from '@/main';
const user_image_path = `../assets${store.state.user.image}`
const user_image = new URL(user_image_path, import.meta.url).href
</script>

<template>
    <EditProfile v-if="showEditProfile" @close="closeEditProfile" />
    <div class="container" v-if="$store.state.user">
        <div class="logo"><img :src= logo ></div>
        <div id='searchbar' class="search">
            <form @submit.prevent="openSearchResult">
            <div>
                <input id='searchbar' type="search" v-model="searchBarTerm" name="query" placeholder="Search . . ." required>
                <button type="submit" id="searchbutton"></button>
            </div>
            </form>
        </div>
        <div class="nav-links">
            <ul>
                <li class="dropdown-li"><div class="dropdown">
                    <div style="display: flex; align-items: center; gap: 5px; font-size: 16px;">{{ $store.state.user.name }}
                        <img :src=user_image alt="" class="user_dp "></div>
                        <div class="dropdown-content">
                            <a v-on:click="openEditProfile">Edit Your Profile</a>
                            <router-link :to="{ name: 'Logout' }">Logout</router-link>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
    <SearchResult :searchTerm="searchBarTerm" v-if="showSearchResult" @close="closeSearchResult" />
</template>

<style scoped>
div.container {
    background-color: #ff7357;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    padding: 0 20px;
    color: #fff;
    position: sticky;
    top: 0;
    z-index: 2;    
}

div.logo > img {
    height: 80px;
    width: 80px;
    z-index: -1;
    border-radius: 1000px;
}

.user_dp {
    height: 50px;
    width: 50px;
    border-radius: 1000px;
}

#searchbar > form > div {
    display: inline-block;
    position: relative;
    filter: drop-shadow(0 1px #0091c2);
    margin-top: -12px;
  }
  
  #searchbar > form > div:after {
    content: "";
    background: white;
    width: 4px;
    height: 12px;
    position: absolute;
    top: 26px;
    right: 0px;
    transform: rotate(135deg);
  }
  
  #searchbar > form > div > input {
    color: white;
    font-size: 12px;
    background: transparent;
    width: 30px;
    height: 30px;
    padding: 10px;
    border: solid 3px white;
    outline: none;
    border-radius: 35px;
    transition: width 0.5s;
  }
  
  #searchbar > form > div > input::placeholder {
    color: white;
    opacity: 0;
    font-size: 12px;
    transition: opacity 150ms ease-out;
  }
  
  #searchbar > form > div > input:focus::placeholder {
    opacity: 1;
  }
  
  #searchbar > form > div > input:focus,
  #searchbar > form > div > input:not(:placeholder-shown) {
    width: 250px;
  }
  #searchbar > form > div > button {
    display: none;
    position: absolute;
    top: 5px;
    right: 5px;
    border: none;
    background: transparent;
    color: white;
    cursor: pointer;
    
  }
  #searchbar:focus + #searchbutton{
    display: block;
    
  }
.nav-links ul {
    display: flex;
    flex-direction: row;
    gap: 0px;
    list-style-type: none;
    width: 100%;
    margin: 0;
    justify-content: flex-end;
    align-items: center;
    box-sizing: border-box;
    top: 0;
    padding: 0;
}
.nav-links li {
    border: 2px solid transparent;
    
    background-color: transparent;
    color: white;
    font-size: 16px;
    padding: 10px 15px;
    border-radius: 4px;
    margin-left: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    
}
.nav-links li:hover {
    border: solid 2px #f9f9f9;
    border-radius: 40px;
}
.nav-links a, .nav-links router-link {
    text-decoration: none;
}
.dropdown {
    border-radius: 1000px;
    
    position: relative;
    display: inline-block;
  }
  
  

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 220px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    border-radius: 10px;
    z-index: 1;
    top: 107%; 
    right: -12px; 
    
  }
  
 
  .dropdown-content a {
    color: black;
    padding: 22px 26px;
    text-decoration: none;
    border-radius: 10px;
    display: block;
  }
  

  .dropdown-content a:hover {
    background-color: #e7e7e7;
  }
  
 
  .dropdown-li:hover .dropdown-content {
    display: block;
    
  }
</style>


<script>
export default {
  data() {
    return {
      showEditProfile: false,
      showSearchResult: false,
      searchBarTerm: ''
    }
  },
  methods: {
      openEditProfile() {
          this.showEditProfile = true;
      },
      closeEditProfile() {
          this.showEditProfile = false;
      },
      openSearchResult() {
          this.showSearchResult = true;
      },
      closeSearchResult() {
          this.showSearchResult = false;
      },
  }
}
</script>