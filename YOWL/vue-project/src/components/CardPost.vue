<template>
  <div class="bg-white dark:bg-gray-800 w-2/4 h-85 p-4 rounded-[30px] shadow-YOWL dark:shadow-YOWL-dark">
    <div class="text-[30px] pb-4 ">
      {{ post.Title }}
    </div>
    <div class="flex flex-col md:flex-row ">
      <img class=" w-44 h-44 object-cover border-2 dark:border-white dark:border-opacity-20 border-black/1 rounded-[15px]"
        :src="'http://10.134.198.105:1337' + post.image.data[0].attributes.url" alt="" />
      <div class="flex flex-col justify-start w-screen pl-6 pr-6">
        <p class="text-[#8A8A8D] text-[base] mb-4 break-all">
          {{ post.description }}
        </p>
        <p class="mb-4 text-base">
          {{ post.author_comment }}
        </p>
        <div class="flex flex-wrap items-center justify-between h-full place-content-end">
          <div class="flex space-x-4">
            <img class="" id="like" src="../assets/Thumb up.svg"/>
            <p class="align-text-bottom pt-0.5">{{ post.like }}</p>
            <button id="show-modal" @click="showModal = true">
              <img href="/comments" id="CommentsView" src="../assets/Comment.svg"/>
              <p class="align-text-bottom pt-0.5">{{ post.comment }}</p>
            </button>
          </div>
          <div>
            <p class="text-[#8A8A8D] text-sm pl-1">posted at {{ post.date }} </p>
          </div>
        </div>
      </div>
    </div>
  </div>
    <modal :show="showModal" :post="post" @close="showModal=false">
      <template>
      </template>
    </modal>
</template>

<script>
import Modal from './ModalView.vue'
export default {
  name: "CardPost",
  props: ["post"],
  components:{
    Modal
  },
  data(){
    return{
      showModal: false
    }
  }
};
</script>

<style scoped>
#like {
  display: block;
  cursor: pointer;
}
#like:active {
  content: url("../assets/Thumb up fill.svg");
  width: 26px;
  width: 26px;
  scale: 1.12;
}
</style>
