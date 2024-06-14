<template>
    <Transition name="modal">
        <div v-if="show">
            <div id="Modal" class="absolute z-10 flex items-center justify-center w-screen h-screen overflow-hidden">
                <div class="flex bg-white dark:bg-gray-800 w-2/3 h-85 pt-4 pb-4 pl-4 rounded-[30px] shadow-YOWL">
                    <div class="w-1/2 border-r-2 border-black border-solid">
                        <div class="text-[30px] pr-4 pb-4 ">
                            {{ post.Title }}
                        </div>
                        <div class="flex flex-col md:flex-row ">
                            <img class=" w-full h-full md:h-auto object-cover md:w-48 border-2 border-black/1 rounded-[15px]" :src="'http://10.134.199.206:1337' + post.image.data[0].attributes.url" alt="" />
                            <div class="flex flex-col justify-start pl-6 pr-6">
                                <p class="text-[#8A8A8D] text-base mb-4 break-all">
                                    {{ post.description }}
                                </p>
                                <p class="mb-24 text-base break-all">
                                    {{ post.author_comment }}
                                </p>
                                <div class="flex flex-wrap items-center justify-between">
                                    <div class="flex space-x-4">
                                        <img class="w-7 h-7" src="../assets/Thumb up.svg"/>
                                        <p class="align-text-bottom pt-0.5">{{ post.like }}</p>
                                    </div>
                                    <div>
                                        <p class="text-[#8A8A8D] text-sm pl-1">posted at {{ post.date }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex overflow-auto w-[32rem] h-[380px] form-control">
                        <div>
                    <CommentsInModalViewVue></CommentsInModalViewVue>
                    <CommentsInModalViewVue></CommentsInModalViewVue>
                    <CommentsInModalViewVue></CommentsInModalViewVue>
                    <CommentsInModalViewVue></CommentsInModalViewVue>
                    <CommentsInModalViewVue></CommentsInModalViewVue>
                        </div>
                        <div class="absolute flex mt-40 ml-2">
                            <input type="text"
                                class="w-[26rem] resize-none mt-60 mb-2 h-10 form-control block px-3 py-1.5 text-base text-gray-700 bg-white dark:bg-gray-800 bg-clip-padding dark:shadow-YOWL-dark rounded-[30px] transition ease-in-out m-0
                                focus:text-gray-700 dark:focus:text-white focus:outline-none"
                                placeholder="Add a comment"/>
                            <button >    
                            <div class="bg-[#15E3A5] rounded-[30px] ml-2 mt-60 mb-2 w-12 h-10 grid justify-items-center items-center">
                                <svg class="p-0.5" width="28" height="26" viewBox="0 0 28 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M5.81163 25.1329C7.43585 25.1329 10.723 23.5561 13.1947 21.7872C21.4639 21.9403 27.6329 17.1705 27.6329 10.9139C27.6329 4.87171 21.6022 0 14.0675 0C6.5307 0 0.5 4.87171 0.5 10.9139C0.5 14.7576 2.89977 18.1973 6.57125 19.98C6.06711 20.9299 5.16711 22.2473 4.65453 22.9219C3.91532 23.9025 4.42742 25.1329 5.81163 25.1329ZM7.21084 22.7616C7.06858 22.8157 7.01444 22.7348 7.10889 22.6085C7.70819 21.8674 8.60772 20.6993 9.03569 19.9008C9.38702 19.2492 9.26491 18.6848 8.51069 18.3269C4.92803 16.6498 2.85451 13.9699 2.85451 10.9139C2.85451 6.19147 7.82913 2.34491 14.0675 2.34491C20.3134 2.34491 25.288 6.19147 25.288 10.9139C25.288 15.6267 20.3134 19.4733 14.0675 19.4733C13.85 19.4733 13.5247 19.4637 13.1108 19.4541C12.6101 19.4541 12.233 19.6001 11.7666 19.9706C10.3547 21.0136 8.25616 22.3385 7.21084 22.7616Z" fill="white"/>
                                    <path d="M14.0772 16.9169C14.6772 16.9169 15.1143 16.4988 15.1143 15.9168V10.3706L15.0058 7.95154L16.0872 9.28725L17.392 10.6471C17.5633 10.8461 17.8101 10.9471 18.0953 10.9471C18.6433 10.9471 19.0563 10.5501 19.0563 10.0106C19.0563 9.73608 18.9583 9.51038 18.7722 9.30624L14.9078 5.39452C14.6577 5.13601 14.4058 5.00195 14.0772 5.00195C13.7678 5.00195 13.5159 5.1264 13.2562 5.39452L9.38218 9.30624C9.19398 9.51038 9.11523 9.73608 9.11523 10.0106C9.11523 10.5501 9.51859 10.9471 10.0666 10.9471C10.3443 10.9471 10.6028 10.8365 10.7699 10.6471L12.0885 9.2767L13.1486 7.97076L13.0401 10.3706V15.9168C13.0401 16.4988 13.4868 16.9169 14.0772 16.9169Z" fill="white"/>
                                </svg>
                            </div>
                        </button> 
                        </div>
                    </div>
                </div>
                <button class="rounded-full shadow-YOWL dark:shadow-YOWL-dark flex items-center place-content-center justify-between fixed text-center text-[21px] bg-white dark:bg-gray-800 w-79 h-[65px] right-4 bottom-8 border-4 border-transparent pr-4 p-1 modal-default-button" @click="$emit('close')">
                    <RouterLink to="/">
                    <img class="pr-4 w-18 h-18" src="../assets/Cross.svg" />
                    </RouterLink>
                    Close
                </button>
            </div>
        </div>
    </Transition>
</template>


<script>

import { Transition } from 'vue';
import CommentsInModalView from './CommentsInModalView.vue';

export default {
    name: 'ModalView',
    components: {
    CommentsInModalViewVue: CommentsInModalView,
    Transition
},
    props: ["post","show"],
}
</script>

<style scoped>
#Modal {
width: 100%;
height: 100%;
backdrop-filter: blur(8px);
background-color: #00000030;
top: 0;
position: fixed;
left: 0;
display: flex;
justify-content: center;
align-items: center;
}
</style>