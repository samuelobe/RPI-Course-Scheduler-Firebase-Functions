import * as functions from 'firebase-functions';
import * as rp from 'request-promise';

const url = 'https://sis.rpi.edu/reg/zs20200501.htm';

export const getHTML = functions.https.onRequest((request, response) => {
    rp(url)
        .then(function (html) {
            //success!
            response.send(html);
            console.log(html);
        })
        .catch(function (err) {
            //handle error
        });

});