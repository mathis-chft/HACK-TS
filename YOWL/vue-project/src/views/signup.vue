<template>
<body class="bg-white align dark:bg-gray-800">
  <div class="login">

    <img class="w-90 h-90 pb-[30px]" src="../assets/YOWL logo dark.svg"/>

    <header class="login__header">
      <h2>
        <svg class="icon">
          <use xlink:href="#icon-lock"/>
        </svg>
        Sign Up
      </h2>
    </header>

    <form @submit.prevent="register" class="text-gray-600 bg-white login__form dark:bg-gray-800 shadow-YOWL dark:text-gray-300 dark:shadow-YOWL-dark" method="POST">
      <div>
        <label for="fullname">Full name</label>
        <input
          class="text-gray-600 bg-gray-200 dark:bg-gray-700 dark:shadow-YOWL-dark shadow-YOWL"
          type="text"
          id="full name"
          name="Full name"
          placeholder="Full name"
          v-model="user.username"
        />
      </div>
      <div>
        <label for="email">E-mail address</label>
        <input
          class="text-gray-600 bg-gray-200 dark:bg-gray-700 dark:shadow-YOWL-dark shadow-YOWL"
          type="email"
          id="email"
          name="email"
          placeholder="mail@address.com"
          v-model="user.email"
        />
      </div>

      <div>
        <label for="password">Password</label>
        <input
          class="text-gray-600 bg-gray-200 dark:bg-gray-700 dark:shadow-YOWL-dark shadow-YOWL"
          type="password"
          id="password"
          name="password"
          placeholder="password"
          v-model="user.password"
        />
        
      </div>

      <div class="flex justify-center">

        <button type="submit" class="rounded-full bg-[#15E3A5] text-white h-8 w-20">Sign Up</button>

      </div>

      <div class="space-x-1.5 dark:text-white">
              <a>Already have an account ?</a>
              <a href="/signin" class="underline dark:text-white underline-offset-2">Sign In</a>
            </div>
    </form>
  </div>

  <svg xmlns="http://www.w3.org/2000/svg" class="icons">
    <symbol id="icon-lock" viewBox="0 0 448 512">
      <path
        d="M400 224h-24v-72C376 68.2 307.8 0 224 0S72 68.2 72 152v72H48c-26.5 0-48 21.5-48 48v192c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V272c0-26.5-21.5-48-48-48zm-104 0H152v-72c0-39.7 32.3-72 72-72s72 32.3 72 72v72z"
      />
    </symbol>
  </svg>
  <CancelButton></CancelButton>
</body>
</template>

<script>
import axios from "axios"
import CancelButton from '../components/CancelButton.vue'

export default {
  name: "Addpost",
      components: {
        CancelButton
      },
  data () {
  return {
    user: {}
  }
},
mounted(){
  console.log("mounted");
},
methods: {
  register() {
    console.log("test");
    axios
    .post('auth/local/register', this.user)
    .then(function(response){
      console.log(response.data.jwt)
      console.log("user registered")
    })
  }
}
}
</script>

<style scoped>
  * {
    font-family: 'Neue Montreal Bold';
    box-sizing: inherit;
  }

  html {
    box-sizing: border-box;
  }

  body {
    position:fixed;
    top:0px;
    bottom:0px;
    left:0px;
    right:0px;
    height: fit-content;
    overflow: auto;
    font-family: "Varela Round", sans-serif;
    line-height: 1.5;
    margin: 0;
    min-block-size: 100vh;
    padding: 5vmin;
  }

  h2 {
    font-size: 1.75rem;
  }

  input {
    background-image: none;
    border: none;
    margin: 0;
    padding: 0;
    transition: all 0.3s;
  }

  svg {
    height: auto;
    max-width: 100%;
    vertical-align: middle;
  }

  /* ---------- ALIGN ---------- */
  .align {
    display: grid;
    place-items: center;
  }

  /* ---------- ICONS ---------- */
  .icons {
    display: none;
  }

  .icon {
    fill: currentcolor;
    display: inline-block;
    height: 1em;
    width: 1em;
  }

  /* ---------- LOGIN ---------- */
  .login {
    width: 400px;
  }

  .login__header {
    background-color: #15E3A5;
    border-top-left-radius: 1.25em;
    border-top-right-radius: 1.25em;
    color: #fff;
    padding: 1.25em 1.625em;
  }

  .login__header :first-child {
    margin-top: 0;
  }

  .login__header :last-child {
    margin-bottom: 0;
  }

  .login h2 .icon {
    margin-right: 14px;
  }

  .login__form {
    border-bottom-left-radius: 1.25em;
    border-bottom-right-radius: 1.25em;
    display: grid;
    gap: 0.875em;
    padding: 1.25em 1.625em;
  }

  .login input {
    outline: none;
    border-radius: 9999px;
  }

  .login input[type="text"],
  .login input[type="email"],
  .login input[type="password"] {
    padding: 0.25em 0.625em;
    width: 100%;
  }

  .login input[type="submit"] {
    display: block;
    margin: 0 auto;
  }
</style>
