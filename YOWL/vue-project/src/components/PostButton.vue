<template>
  <button
    class="rounded-full shadow-YOWL dark:shadow-YOWL-dark flex items-center place-content-center bg-[#15E3A5] justify-between fixed text-center text-[21px] text-white w-79 h-[65px] right-48 bottom-8 border-4 border-[#15E3A5] pr-4 p-1">
    <RouterLink to="/">
      <img class="pr-4 w-18 h-18" src="../assets/Check.svg" />
    </RouterLink>
    Post
  </button>
</template>
<script>
  export default {
    name: "PostButton",
  }
</script>