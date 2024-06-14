<template>
  <h1 class="flex justify-center text-[40px] pt-[5%] pb-4">New post</h1>


  <div class="flex justify-center">
    <div class=" bg-white dark:bg-transparent w-2/4 h-auto p-4 rounded-[30px]">
      <div class="flex justify-center">
        <div class="mb-3 xl:w-96">
          <label for="exampleURL0" class="inline-block pt-2 mb-2 text-black dark:text-white form-label">
            Title
          </label>
          <input type="url"
            class="form-control block w-full px-3 py-1.5 text-base text-black  bg-white dark:bg-gray-800 dark:text-gray-200 bg-clip-padding border 
               border-transparent shadow-YOWL dark:shadow-YOWL-dark rounded-full transition ease-in-out m-0
                focus:text-gray-700 dark:focus:text-white focus:outline-none"
            id="exampleURL0" placeholder="Enter your title"/>
        </div>
      </div>

      <div class="flex justify-center">
        <div class="mb-3 xl:w-96">
          <label for="exampleURL0" class="inline-block pt-2 mb-2 text-black dark:text-white form-label">
            Link of the video, article, movie...
          </label>
          <input type="url"
            class="form-control block w-full px-3 py-1.5 text-base text-black bg-white dark:bg-gray-800 dark:text-gray-200 bg-clip-padding border 
               border-transparent shadow-YOWL dark:shadow-YOWL-dark rounded-full transition ease-in-out m-0
                focus:text-gray-700 dark:focus:text-white focus:outline-none"
            id="exampleURL0" placeholder="Insert your link"/>
        </div>
      </div>

      <div class="flex justify-center">
        <div class="mb-3 xl:w-96">
          <label for="exampleText0" class="inline-block pt-2 mb-2 text-black dark:text-white form-label">
            Description
          </label>
          <textarea type="text"
            class="resize-none pt-3 pb-24 h-8 form-control block w-full px-3 py-1.5 text-base text-gray-700 bg-white dark:bg-gray-800 dark:text-gray-200 bg-clip-padding
            border-transparent shadow-YOWL rounded-[30px] transition ease-in-out m-0
            focus:text-gray-700 dark:focus:text-white focus:outline-none"
            placeholder="What are you going to talk about today ?"/>
        </div>
      </div>
      
      <div class="flex justify-center">
        <div class="mb-8 xl:w-96">
          <label for="exampleText0" class="inline-block pt-2 mb-2 text-black dark:text-white form-label">
            Comment
          </label>
          <textarea type="text"
            class="resize-none pt-3 pb-24 h-8 form-control block w-full px-3 py-1.5 text-base text-gray-700 bg-white dark:bg-gray-800 dark:text-gray-200 bg-clip-padding
            border-transparent shadow-YOWL dark:shadow-YOWL-dark rounded-[30px] transition ease-in-out m-0
            focus:text-gray-700 dark:focus:text-white focus:outline-none"
            placeholder="Something to say about it ?"/>
        </div>
      </div>

      <div class="flex justify-center space-x-28">
        <div class="flex justify-center">
          <div class="flex items-center justify-center">
            <DropdownMenu/>
          </div>
        </div>

        <div class="flex items-center justify-center ">
          <label class="border-transparent label dark:bg-gray-800 shadow-YOWL">
          <input type="file" id="myfile" accept="image/*" class="flex items-center justify-center w-56 h-12 text-black rounded-full ">
          <span class="text-sm text-black dark:text-white">Upload image</span>
          </label>
        </div>
      </div>

      <div class="justify-between">
        <PostButton></PostButton>
        <CancelButton></CancelButton>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import DropdownMenu from '../components/DropdownMenu.vue'
import CancelButton from '../components/CancelButton.vue'
import CardPost from '../components/CardPost.vue'
import PostButton from '../components/PostButton.vue'
export default {
  name: "Addpost",
  components: {
    DropdownMenu,
    CancelButton,
    CardPost,
    PostButton
},
  data() {
    return {
      content_post: null,
    }
  },
mounted (){
  axios.post('')
}
}


</script>

<style scoped>
label.label input[type="file"] {
  position: absolute;
  top: -1000px;
}
.label {
  cursor: pointer;
  border-radius: 9999px;
  padding: 10px 16px;
  margin: 5px;
  display: inline-block;
}
</style>