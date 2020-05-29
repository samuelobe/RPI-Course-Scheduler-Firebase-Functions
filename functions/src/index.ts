//import * as functions from "firebase-functions";
import * as axios from "axios";
import * as cheerio from "cheerio";
import { Course } from "./course";
import { writeFileSync } from "fs";

const url = "https://sis.rpi.edu/reg/zs202009.htm";

axios.default
  .get(url)
  .then((res) => {
    const $ = cheerio.load(res.data);
    const text = $("tr").text();
    const items = text.split("\n\n");
    const courseArray: Array<Course> = [];


    // tslint:disable-next-line:prefer-for-of
    for (let index = 0; index < items.length; index++) {
      if (items[index].includes("\n")) {
        items[index] = items[index].replace("\n", "");
      }

      if (items[index] === "CRN") {
        items.splice(index, 26);
      }
      if (items[index] === "View TextBooks") {
        items.splice(index, 1);
      }
    }
    console.log(items);
    //let i: number = 0;
    for (let index = 1; index < items.length; index += 15) {
      courseArray.push(
        new Course(
          items[index],
          items[index + 1],
          items[index + 2],
          items[index + 3],
          items[index + 4],
          items[index + 5],
          items[index + 6],
          items[index + 7],
          items[index + 8],
          items[index + 9],
          items[index + 10],
          items[index + 11]
        )
      );
      //console.log(courseArray[i].print());
      //i++;
    }
    let logString : string ="";
    items.forEach(element => {
      logString += element + "\n";
    });
    writeFileSync("./filename.txt", logString);
    //console.log(logString);
  })
  .catch(() => console.log("poop"));


/*
export const getHTML = functions.https.onRequest((request, response) => {

});
*/
