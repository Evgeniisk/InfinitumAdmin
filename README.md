This is InfinitumAdmin web application MSc Computing and Information Systems (conversion) major project developed by Evgenii Korostelev, Student ID: 200251127.

This project provides a prototype solution for streamling, automating, centralising and making it easier for business to administrate their companies implemented as a full-stack web application. (Refer to the dissertation, demo video and reflective essay for full project details).

When you download this project folder, please rename the folder from InfinitumAdmin-main to InfinitumAdmin as the name may affect the way the code works when it has to navigate and access directories in the project.


PERSONAL SECURITY CONSIDERATIONS

I did put some personal details that should be kept secret such as the keys to my development DocuSign API account and the authentication details to my gmail SMTP server account. I left them there for you (the assessors) to have the most comfortable experience when marking this project. Could you please not share the details that should be kept secret with anyone, not use them in an unethical way and delete or not save them after marking the project. Thank you.

I am also submitting this project through a public github repository because I didn't know how I could give you the full code with sensitive information that should be kept secret and I didn't want to miss the submission deadline. In light of this, if you could, could you please tell me after you downloaded the project for marking, tell me you did so, and if it possible, if you could let me know if I can delete the public repository for this project from github. Additionally, I will change all the secret keys and accounts I used in this web application after it is marked for security reasons.


NOTE ON DOCUSIGN

Because this is not a production grade application and I didn't have money to spend the DocuSign API is used in development mode. To use this application to it's full potential you must connect a DecuSign account to this web app. Because this application is made using docusign development account, you must create a docusign development account to connect your account to my application to use it.

If you have any questions about this, please don't hesitate to contact me.


Installation Instructions:

Please note that this application was developed on windows operating system, and would work best with a windows operating system. This is because all the code that modifies or makes use of file directories is tailored only for windows operating system.

To run this project in development environment you need to create a virtual environment for this project, activate it, install the requirements.txt file using "pip install -r requirements.txt" command while cdd into the backend folder.
You need to also run the "npm install" command while cdd into the front end folder of the web application.
Then you need to download libre office onto your computer, you can do this using this link: https://www.libreoffice.org/download/download-libreoffice/?lang=en-US&type=win-x86&version=24.8.7 because this application uses libre office to convert word files to pdf files (refer to MainApp.views file and the replace_placeholders_invoice function in that file which is defined on line 1565 of the file) (in that function refer to lines starting from 1677 until the end of the function which has code that makes use of libraoffice)
Then while cdd into the backend folder you need to run "python manage.py makemigrations" command and then run "python manage.py migrate" command straight after. If there are issues with migrations, try to delete all the migration files except from the inital migration files from migration folder in both the backend and frontend folders
Then you need to have two terminals, one cdd into the front end folder and the other cdd into the backend folder
Then in the terminal cdd into the backend folder you need to run "python manage.py runserver" command
Then in the terminal cdd into the frontend folder you need to run "npm run dev" command
Then you can click on the link shown in the terminal that is cdd into the backend folder to start exploring the app, making an account etc.
This application uses an authentication system that requires sending confirmation codes, so if you register an account, register it with a real email addess for a smooth experience.

The user interface is friendly and intuitive so no instructions are needed for using the app and there are pop ups and instructions across the app guiding the user on how to use it


Notes on Comments:

Most of the code in the python files is commented

Most of the files in the front end are commented, but the comments in the vue files are mostly in the script sections of the files because they are easier to comment and they handle most of the functionality on the pages.

Any comment you see on a line that doesn't have code in it is commenting the code on the lines below it.

If you have any questions about any code in this project, please don't hesitate to contact me.


Testing instructions:

For testing this application I used Django's LiveServerTestCase and selenium to test the basic functionality and security of the application along with it's UI as if it is is production.
Because of this to test the application you need to go into the backend.AuthenticationApp.views.login_user function and comment out the second "retun redirect" line (line 342) that looks like this: return redirect('http://localhost:5173/') in that function and uncomment the line below it (line 343). Then go to the backend.InfinitumAdmin.urls file and uncomment the last two entries of the urlpatterns list in that file (lines 30 & 31).

To test it with full security insurance you need to additionally comment out the cors middleware and configurations from the settings. This is how I tested this application ensuring it is secure and it did pass all the tests. But just following the instructions above will also work.

I user firefox browser and its driver to test the application. The drivers for firefox browsers can be found here: https://github.com/mozilla/geckodriver/releases.

Then when ccd into the backend folder just run "python manage.py test AuthenticationApp" command in the terminal and that should show the testing in front of you in the browser. When the browser pop up not testing will take place for a few seconds (maybe 10 secs max), please just wait for it to start. This is because as part of testing the npm run build command is dynamically called to enable cumfortable testing of the app as if it is in production.

To use the application in development reverse the instructions described above and run the "npm run dev" command while ccd into the frontend folder again (this is important because if you don't do this and use the development server that is running from before testing has taken place then the settings and urls will have deployment environment variables instead of the development ones) and it should be good to go for development mode.

To test the con jobs algorithms cdd in the backend folder and run the following command: "python manage.py invoice_automations"


Deployment

This app is deployed on my home computer and it is available online at https://infinitumadmin.duckdns.org it is deployed securely and you can try to test the live deployed application for security vulnerabilities. There is a problem with the deployed application which is that it doesn't allow for feedback on successfull signature of contracts in deployment because of the <iframe> tag, more information on this is in the dissertation, the reflective essay and at the end of the video demonstration. If you do successfully hack my web application or my computer or my network please let me know.


All the references for everything used in this project can be found in the dissertation and the reflective essay.
