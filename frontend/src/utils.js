//This function retrives the value of a scp
export function CookieHandle(name) {
    let cookiestring = null;
    //If there are cookies in the document and they are not empty
    if (document.cookie && document.cookie !== '') {
        //Splits cookies in and array
        const cookies = document.cookie.split(';');
        //loops through the cookies array
        for (let cookie of cookies) {
            //removes any spaces from the cookie string
            cookie = cookie.trim();
            //checks if the cookie starts with the passed name value followed by =
            if (cookie.startsWith(name + '=')) {
                //extracts the value of the cookie and decodes it because it is encoded by broswer, so I need to decode it
                cookiestring = decodeURIComponent(cookie.split('=')[1]);
                break;
            }
        }
    }
    //retuns the cookie value
    return cookiestring;
}

const csrftoken = CookieHandle('csrftoken');