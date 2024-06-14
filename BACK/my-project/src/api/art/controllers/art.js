'use strict';

/**
 * art controller
 */
const { createCoreController } = require('@strapi/strapi').factories;
module.exports = createCoreController('api::art.art', ({ strapi }) => ({
    async create(ctx) {
        const { data } = ctx.request.body;
        data.author_user = ctx.state.user.id;
        const response = await strapi.entityService.create(
           "api::art.art",
           {
             data: data,
           } 
         );
        return {response}
       },
    async update (ctx){ 
        const {data} = ctx.request.body;
        const entry = await strapi.service('api::art.art').findOne (ctx.params.id,{
            populate: { author_user: true },
      
          });
          if (ctx.state.user.id == entry.author_user.id){
            const response = await strapi.service('api::art.art').update(ctx.params.id,
      
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
        const entry = await strapi.service('api::art.art').findOne (ctx.params.id,{
            populate: { author_user: true },
      
          });
          if (ctx.state.user.id == entry.author_user.id){
            const response = await strapi.service('api::art.art').delete(ctx.params.id,
      
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
      
      
     }))