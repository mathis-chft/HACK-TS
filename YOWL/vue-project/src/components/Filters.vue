<template>
  <div
    class="fixed text-lg bg-white dark:bg-gray-800 w-60 right-4 rounded-[30px] border-4 border-transparent pr-10 p-4 shadow-YOWL dark:shadow-YOWL-dark"
  >
    Filters
    <div class="flex items-center mt-1 ml-2">
      <div>
        <div class="flex items-center mt-4 form-check">
          <input
            class="form-check-input appearance-none rounded-full h-4 w-4 border-black-600 border-2 checked:bg-[#15E3A5] checked:border-none focus:outline-black-400 transition duration-100 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault1"
            checked
          />
          <label
            class="inline-block ml-2 form-check-label text-black-800"
            for="flexRadioDefault1"
          >
            New
          </label>
        </div>
        <div class="flex items-center mt-4 form-check">
          <input
            class="form-check-input appearance-none rounded-full h-4 w-4 border-black-600 border-2 checked:bg-[#15E3A5] checked:border-none focus:outline-black-400 transition duration-200 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer"
            type="radio"
            name="flexRadioDefault"
            id="flexRadioDefault2"
          />
          <label
            class="inline-block ml-2 form-check-label text-black-800"
            for="flexRadioDefault2"
          >
            Popular
          </label>
        </div>
      </div>
    </div>
  </div>
</template>
