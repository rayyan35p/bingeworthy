# bingeworthy

Unfortunately, we weren't able to upload the app onto Heroku for now so if you would like to try
the app, do follow these steps:
---
1. Download all the code and unzip if necessary to another folder
2. Open command prompt/terminal at the folder 
3. Create a virtual environment by typing `python3 -m venv venv`
4. Activate the virtual environment by typing
    `source venv/bin/activate` for mac
    `venv\Scripts\activate.bat` for windows
    *(do google online if it doesn't work as we are using mac)*
    and there should now be a (venv) on the command line
5. Install the requirements using `pip3 install -r requirements.txt`
6. After all the requirements have been installed, run the app using `flask run`
7. If there is an error, try deactivating the virtual environment using `deactivate`
    and reactivating as per step 4. After which, try `flask run` again.
8. The app should now launch. Looking forward to your feedback!