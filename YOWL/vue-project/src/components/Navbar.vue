<template>
  <nav class="flex items-center">
    <ul
      class="fixed flex pl-4 pt-8 pr-4 pb-10 w-screen justify-between items-center h-[120px] backdrop-blur-[100px]"
      style="left: 0px !important; top: 0px !important;">

      <router-link to="/">
        <img class="w-48 h-48" src="../assets/YOWL logo dark.svg" />
      </router-link>

      <div class="text-[#8A8A8D] dark:text-white flex justify-center items-center h-auto">
        <div class="xl:w-[620px] ml-3 mr-3">
          <div class="relative flex flex-wrap items-center content-center justify-between w-full rounded input-group">
            <div class="container">
            <form class="nosubmit h-14">
              <input class="nosubmit shadow-YOWL dark:shadow-YOWL-dark " type="search" placeholder="Search comments">
            </form>
            </div>
          </div>
        </div>
      </div>
      <router-link to="/signin">
        <button
          class="flex w-60 text-lg bg-white dark:bg-gray-800 h-14 items-center justify-between rounded-[30px] border-4 border-transparent p-4 shadow-YOWL dark:shadow-YOWL-dark">
          <div class="flex items-center">
            <img class="mr-4" src="../assets/Profile pic.svg ">
            Login
          </div>
          <div>
            <img src="../assets/chevron.right.circle.svg">
          </div>
        </button>
      </router-link>
    </ul>
  </nav>
</template>


<style scoped>


form {
  display: flex;
  border-radius: 9999px;
}

input[type=search] {
  padding: 7px 8px;
  font-size: 18px;
  border-radius: inherit;
}

form.nosubmit {
  border: none;
  padding: 0;
}

input.nosubmit {
  width: 100%;
  padding: 0px 7px 0px 50px;
  background: transparent url("../assets/magnifier.svg") no-repeat 13px center;
}

input.nosubmit:focus {
  outline: none;
}
</style>

