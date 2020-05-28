import * as functions from "firebase-functions";
import * as axios from "axios";
import * as cheerio from "cheerio";

const url = "https://sis.rpi.edu/reg/zs20200501.htm";

export const getHTML = functions.https.onRequest((request, response) => {
  axios.default
    .get(url)
    .then((res) => {
      const $ = cheerio.load(res.data);
      
      response.send($("tr").text());
      //console.log(res.data);
    })
    .catch(() => console.log("poop"));
});
