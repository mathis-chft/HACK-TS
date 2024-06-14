<template style="padding-left: 0px !important;" v-if="post">
  <Navbar></Navbar>
  <Categories></Categories>

  <h1 class="text-[40px] pt-[8%] pb-6 pl-[26%]">Home</h1>
  <ul class="grid gap-12 pb-12 place-items-center">
    <CardPost v-for="item in post" :key="item" :post="item.attributes" v-if="post">
    </CardPost>
    <AddPostButton></AddPostButton>
    <Filters></Filters>
  </ul>
</template>
  
<script>
import CardPost from '../components/CardPost.vue'
import Navbar from '../components/Navbar.vue'
import Categories from '../components/Categories.vue'
import Filters from '../components/Filters.vue'
import AddPostButton from '../components/AddPostButton.vue'
import CancelButton from '../components/CancelButton.vue'
import CommentsInModalView from '../components/CommentsInModalView.vue'
import ModalView from '../components/ModalView.vue'
import axios from "axios"

export default {

  name: "home",
  components: {
    ModalView,
    CommentsInModalView,
    CardPost,
    Navbar,
    Categories,
    Filters,
    AddPostButton,
    CancelButton,
  },

  data() {
    return {
      post: null,
    }
  },
  mounted() {
    axios.get('http://localhost:1337/api/posts?populate=*')
      .then(response => {
        this.post = response.data.data
        console.log(this.post)
      })
  }
}
</script>

