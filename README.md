<div  align="center">
<a href="https://github.com/luissilva1044894/FlaskPyrezAPI" title="FlaskPyrezAPI - Github repository" alt="FlaskPyrezAPI · Github repository"><img src="./static/img/pyrez.png" height="128" width="128"></a>

# FlaskPyrezAPI
[![License](https://img.shields.io/github/license/luissilva1044894/FlaskPyrezAPI.svg?style=plastic&logoWidth=10)](./LICENSE "FlaskPyrezAPI · LICENSE")
[![Runtime Version](https://img.shields.io/pypi/pyversions/flask.svg?style=plastic&logo=python&logoWidth=10)](https://pypi.org/project/pyrez "Python Runtime Versions")
[![Discord Server](https://img.shields.io/discord/549020573846470659.svg?style=plastic&logo=discord&logoWidth=10)](https://discord.gg/XkydRPS "Support Server · Discord")
</div>

**FlaskPyrezAPI** is an [open-source](http://www.opensource.org "See http://www.opensource.org for the Open Source Definition") endpoint for [`Twitch`](https://twitch.tv "Twitch") commands, that provides datas about players, matches and others stats of the game [`Paladins`](https://paladins.com "Paladins Game").

[Demo ![Website](https://img.shields.io/website/https/nonsocial.herokuapp.com.svg)](https://nonsocial.herokuapp.com/)

### Built with
- [Python](https://www.python.org/ "Requires Python 2.7 or 3.x (3.5 or higher)")
- [Pyrez](https://pypi.org/project/pyrez/ "Pyrez · v1.1.0.0 · PyPI") - Used for handling connections and requests to [`Hi-Rez Studios`](https://www.hirezstudios.com) API.
- [Flask](https://pypi.org/project/Flask/ "Flask · v1.0.3 · PyPI")
- [Bootstrap 4](https://getbootstrap.com/docs/4.3/getting-started/introduction/ "Bootstrap · v4.3.1")
- [Font Awesome](https://fontawesome.com/changelog/latest/ "Font Awesome · v5.9")

### Requirements
- [Access](https://pyrez.readthedocs.io/en/stable/gettingstarted.html#registration "Form access to Hi-Rez Studios API") to Hi-Rez Studios API.

### Support
For support using Pyrez, please join the official [*support server*](
https://discord.gg/XkydRPS "Support Server · Discord") on [Discord](https://discordapp.com/ "Discord App").

### Installation
#### Locally
1. Clone this repository: `git clone https://github.com/luissilva1044894/FlaskPyrezAPI.git`
2. ``cd`` into it: `cd FlaskPyrezAPI`
3. Create a virtualenv: `virtualenv -p python venv`
4. Activate it.
5. Install Python Dependencies: `pip install --upgrade pip setuptools wheel` | `pip install -r requirements.txt`
6. Edit [`.env`](./.env) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [`Hi-Rez Studios`](https://luissilva1044894.github.io/Pyrez/docs#registration "Form access to Hi-Rez Studios API").
7. Run server: `python manage.py runserver`
8. Go to your browser and point it towards `http://127.0.0.1:5000`

#### Deploy (Heroku) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/luissilva1044894/FlaskPyrezAPI/tree/master "Deploy to Heroku")
1. Go to [Heroku](https://id.heroku.com/login) and create a new app (eg: `your-app-name`)
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli "Heroku CLI")
3. `heroku login`
4. `git init`
5. `heroku git:remote -a your-app-name`
6. Download this repo and copy all files into `your-app-name` folder
7. Edit [`.env`](./.env) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [`Hi-Rez Studios`](https://luissilva1044894.github.io/Pyrez/docs#registration "Form access to Hi-Rez Studios API").
8. `heroku config:push`
9. `git add .`
10. `git commit -m "Going to Heroku"`
11. `git push heroku master`
12. `heroku run python manage.py db migrate`
13. `heroku open` and a window will open with your app online

### Thanks
* [`Lukash (Paladins Poland)`](https://www.facebook.com/PaladinsPoland/ "Paladins Poland") - Polish translation.

### License
This project is provided under the MIT License, which you can view in [`LICENSE file`](./LICENSE "FlaskPyrezAPI · License").

> Raw data provided by Hi-Rez Studios API and is thus their property. © 2019 Hi-Rez Studios, Inc. All rights reserved.
