<template>
   <body class="bg-white align dark:bg-gray-800">
        <div class="login">

        <img class="w-90 h-90 pb-[30px]" src="../assets/YOWL logo dark.svg"/>
    
        <header class="login__header">
            <h2><svg class="icon">
                <use xlink:href="#icon-lock" />
            </svg>Sign In</h2>
        </header>
    
        <form @submit.prevent="login" class="text-gray-600 bg-white login__form dark:bg-gray-800 dark:text-gray-300 shadow-YOWL dark:shadow-YOWL-dark" >
            
            <div>
            <label for="email">E-mail address</label>
            <input class="text-gray-600 bg-gray-200 dark:bg-gray-700 dark:text-white dark:shadow-YOWL-dark shadow-YOWL" type="email" id="email" name="email" placeholder="email" v-model="identifier">
            </div>
    
            <div>
            <label for="password">Password</label>
            <input class="text-gray-600 bg-gray-200 dark:bg-gray-700 dark:text-white dark:shadow-YOWL-dark shadow-YOWL" type="password" id="password" name="password" placeholder="password" v-model="password">
            </div>
    
            <div class="flex justify-center">
              <button type="submit" class="rounded-full bg-[#15E3A5] text-white h-8 w-20" >{{ !loading ? "Sign In" : "loading ..." }}</button>
            </div>
            
            <div class="space-x-1.5">
              <a class="dark:text-white">Don't have an account ?</a>
              <a href="/signup" class="underline underline-offset-2 dark:text-white">Sign Up</a>
            </div>

        </form>
    



        </div>
    
        <svg xmlns="http://www.w3.org/2000/svg" class="icons">
        <symbol id="icon-lock" viewBox="0 0 448 512">
            <path d="M400 224h-24v-72C376 68.2 307.8 0 224 0S72 68.2 72 152v72H48c-26.5 0-48 21.5-48 48v192c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V272c0-26.5-21.5-48-48-48zm-104 0H152v-72c0-39.7 32.3-72 72-72s72 32.3 72 72v72z" />
        </symbol>
    
        </svg>
    <CancelButton></CancelButton>
    </body>
</template> 

<script>

  import axios from 'axios';
  import CancelButton from '../components/CancelButton.vue'

  export default {
    name: "Addpost",
      components: {
        CancelButton
      },
    data () {
    return {
      identifier: "",
      password: "",
      loading: false
    }
  },
  mounted(){
    console.log("mounted");
  },
  methods: {
    async login() {
      console.log("test");
      this.loading = true
      await axios
      .post('auth/local', {
        identifier: this.identifier,
        password: this.password,
      })
      .then(response => {
        
        localStorage.setItem("jwt", response.data.jwt);
        localStorage.setItem("user",response.data.user.username);
        console.log(response.data);

        this.loading = false
        this.$router.push("/")
      })
      .catch(error => {
        console.log('An error occurred:', error.response);
        localStorage.removeItem("jwt");
        localStorage.removeItem("user")
      });
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
    line-height: 1.5;
    margin: 0;
    padding: 5vmin;
  }
  
  h2 {
    font-size: 1.75rem;
  }
  
  input {
    background-image: none;
    border: none;
    font: inherit;
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
    color: rgb(255, 255, 255);
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
    border-radius: 9999px;
  }
  
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