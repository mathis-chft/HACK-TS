<template>
  <button
    class="rounded-full shadow-YOWL dark:shadow-YOWL-dark flex items-center place-content-center justify-between fixed text-center text-[21px] bg-white dark:bg-gray-800 w-79 h-[65px] right-4 bottom-8 border-4 border-transparent pr-4 p-1">
    <RouterLink to="/">
      <img class="pr-4 w-18 h-18" src="../assets/Cross.svg" />
    </RouterLink>
    Cancel
  </button>
</template>
<script>
  export default {
    name: "CancelButton",
  }
</script>