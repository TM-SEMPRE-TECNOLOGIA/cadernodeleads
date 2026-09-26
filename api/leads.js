// Vercel Serverless Function — API /api/leads
const dataHandler = require('./data');

module.exports = async (req, res) => {
  return dataHandler(req, res);
};
