# Screenshot web-service
## Test project for Craftum.

This is a web service that takes full page screenshots.

* For install all libraries type in console **pip install path/to/requirements.txt**

* For run project locally type in console **source env/bin/activate** and then type **python app.py**

* To work with web services, follow the link to the local server http://127.0.0.1:5000/ and then click on the **Main page**

* Then enter the link, the screenshot you want to take and click **Submit**

* You will get an id. 

* Enter this ID in the link http://127.0.0.1:5000/check/ **id**

* Then you will get screenshot_url. 

* Copy the title under quotes and type in http://127.0.0.1:5000/ **screenshot_url**. 
A screenshot will be downloaded to your computer.

* To run the application on Heroku, type in the console **source env/bin/activate** and later type **heroku run python app.py --app wordcount-pro-19-03-2022**
* Follow in your browser on link **https://wordcount-pro-19-03-2022.herokuapp.com/**