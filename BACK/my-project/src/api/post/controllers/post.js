'use strict';

/**
 * post controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::post.post', ({ strapi }) => ({
    async create(ctx) {
        const { data } = ctx.request.body;
        data.author_user = ctx.state.user.id;
        const response = await strapi.entityService.create(
           "api::post.post",
           {
             data: data,
           } 
         );
        return {response}
       },
    async update (ctx){ 
        const {data} = ctx.request.body;
        const entry = await strapi.service('api::post.post').findOne (ctx.params.id,{
            populate: { author_user: true },
      
          });
          if (ctx.state.user.id == entry.author_user.id){
            const response = await strapi.service('api::post.post').update(ctx.params.id,
      
          {
            data:data,
          }
      )
      return {response}
      }
       else {
      return (" Sorry,you are not allowed to update the post")
       }
      },
      
      async delete (ctx){ 
        const {data} = ctx.request.body;
        const entry = await strapi.service('api::post.post').findOne (ctx.params.id,{
            populate: { author_user: true },
      
          });
          if (ctx.state.user.id == entry.author_user.id){
            const response = await strapi.service('api::post.post').delete(ctx.params.id,
      
          {
            data:data,
          }
      )
      return {response}
      }
       else {
      return (" Sorry,you are not allowed to delete the post")
       }
      },
      
      // delete
    
    // async update(ctx) {
    //     const {data} = ctx.request.body;
    //     data.author_user = ctx.state.user.id;
    //     const author_user = await strapi.entityService.findOne('api::post.post', ctx.params.id, {
    //       populate: {author_user : true},
    //     });
    //     if(author_user.id = ctx.state.user.id ){
    //       console.log(author_user.author_user)
    //       console.log(ctx.state.user.id)
    //       const response = await strapi.entityService.update(
    //         "api::post.post",
    //         ctx.params.id,
    //         {
    //           data: data,
    //         }
    //       );
    //      return {response}
    //     }
    //     else{
    //       ("T'as pas le droit vilain!")
    //     }
    //   },
    //   async delete (ctx){
    //     const {data} = ctx.request.body;
    //     data.author_user = ctx.state.user.id;
    //     const author_user = await strapi.entityService.findOne('api::post.post', ctx.params.id, {
    //       populate: { author_user : true },
    //     });
    //     if(author_user.author_user.id=ctx.state.user.id){
    //       const response = await strapi.entityService.delete(
    //         "api::post.post", 
    //         ctx.params.id,
    //         {
    //           data: data,
    //         }
    //       );
    //      return {response}
    //     }
    //     else{
    //       ("T'as pas le droit vilain!")
    //     }
    //   },
     }))