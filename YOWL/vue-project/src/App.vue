<script setup>
import { RouterView } from "vue-router";

</script>

<template>
  <body>
    <div id="test"></div>
    <RouterView/>
  </body>
</template>

<style>
@media (prefers-color-scheme: light) {
    html {
        background: white;
    }
}

@media (prefers-color-scheme: dark) {
  html {
        Background: rgb(31, 41, 55);
        color: rgb(255, 255, 255); 
   }
}
</style>