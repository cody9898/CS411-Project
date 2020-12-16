# CS411-Project
Web app for CS411 project (team 10)

Group members: Dakota Clark-Singh, Adam Chrysostomou, Anthony Chang, Gabriel Belmont, Stephany Yipchoy, Wail Attauabi.

# Demo Link
https://drive.google.com/file/d/11LTY8g0b8zrYqC339CHA1XAS3alG-fMI/view?usp=sharing

# How to run

To start server:

Navigate to project folder in terminal 

First install pip

Install pip on windows:
```
py -m pip install --upgrade pip
```

Install pip on Linux/macOS:
```
python3 -m pip install --user --upgrade pip
```
Next, install virtual environment 

On windows:
```
py -m pip install --user virtualenv
```

On macOS:
```
python3 -m pip install --user virtualenv
```

Install requirements:
```
pip install -r requirements.txt
```

Go into server directory

Create a virtual environment

Windows:
```
py -m venv env
```

macOS and Linux:
```
python3 -m venv env
```

Activate the virtual environment

Windows:
```
.\env\Scripts\activate
```

macOS/Linux:
```
source env/bin/activate
```

Within the virtual environment: 
```
pip install requests
pip install flask
pip install flask_Cors
pip install PyYAML
python app.py
```

Control-C to stop server from running on local 

To start client: 
Go into client directory in terminal 

Install homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
```
yarn global add @vue/cli
yarn add @vue/cli-service
yarn add vue2-google-maps
```

To run client:
```
yarn serve
```

Control-C to stop server from running on local 
