'use strict';

/**
 * gaming service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::gaming.gaming');
