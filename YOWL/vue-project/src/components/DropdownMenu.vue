<template>
    <button id="dropdownRadioButton" data-dropdown-toggle="dropdownDefaultRadio" class="text-black dark:text-white bg-white dark:bg-gray-800 border-white shadow-YOWL dark:shadow-YOWL-dark focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm px-4 py-2.5 text-center inline-flex items-center" type="button">Categories <svg class="w-4 h-4 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></button>

  <div id="dropdownDefaultRadio" class="z-10 hidden w-48 bg-white divide-y divide-gray-100 rounded shadow">
      <ul class="p-3 space-y-3 text-sm text-gray-700" aria-labelledby="dropdownRadioButton">
        <li>
          <div class="flex items-center">
              <input id="default-radio-1" type="radio" value="" name="default-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500">
              <label for="default-radio-1" class="ml-2 text-sm font-medium text-gray-900">Default radio</label>
          </div>
        </li>
        <li>
          <div class="flex items-center">
              <input checked id="default-radio-2" type="radio" value="" name="default-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500">
              <label for="default-radio-2" class="ml-2 text-sm font-medium text-gray-900">Checked state</label>
          </div>
        </li>
        <li>
          <div class="flex items-center">
              <input id="default-radio-3" type="radio" value="" name="default-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500">
              <label for="default-radio-3" class="ml-2 text-sm font-medium text-gray-900">Default radio</label>
          </div>
        </li>
      </ul>
  </div>
</template>

<script>
  export default {
    name: "DropdownMenu"
  }
</script>