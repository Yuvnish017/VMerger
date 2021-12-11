# VMerger
A Python Flask framework based Web Application for merging video files
### Prerequisites
* Python==3.8.5
* Flask==1.1.2
* Werkzeug==1.0.1
* moviepy==1.0.3
* gunicorn
### Installation and Running Process
* Clone the repository and install all the libraries mentioned in 'requirements.txt' file.
* Run the 'main_app.py' file in command prompt or any IDE
* Copy the localhost URL displayed on running the file.
* Paste the URL in any browser and enjoy playing with the application!!
### Description of files and folders
* main_app.py - the backend server python file
* templates folder - contains the HTML files for web application
* static folder - contains background image and the CSS files.
* requirements.txt - contains list of libraries required with versions
#### Note
* Change line 122 based on working environment - Development or Devployment/Production environment. </br>
  For Development
  
  ```
  app.run(port='5004', debug=True)
  ```
  
  For Deployment
  
  ```
  app.run(host='0.0.0.0')
  ``` 
* Don't forget to turn off debugging mode by debug=False when deploying the application and add host='0.0.0.0' in app.run() again.
* Create an empty folder by the name 'uploads' before running the python file. This folder will be storing the uploaded files.
