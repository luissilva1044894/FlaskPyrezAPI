# FlaskPyrezAPI
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/luissilva1044894/Pyrez/blob/master/LICENSE)
[![Runtime Version](https://img.shields.io/pypi/pyversions/pyrez.svg)](https://pypi.org/project/pyrez)
[![Contributors](https://img.shields.io/github/contributors/luissilva1044894/Pyrez.svg)](https://github.com/luissilva1044894/Pyrez/graphs/contributors)

**FlaskPyrezAPI** is an open-source endpoint for [Twitch](https://twitch.tv) commands, written in Python, that provides datas about players, matches and others stats of the game [Paladins](https://paladins.com). This API uses [Pyrez](https://github.com/luissilva1044894/Pyrez) for handling connections and requests to [Hi-Rez Studios](https://www.hirezstudios.com) API.

## Requirements
* [Python](http://python.org "Python.org") 3.5(or higher).
    * The following libraries are required: [`Requests`](https://pypi.org/project/requests "requests") and `requests-aeaweb`.
- [Access](https://fs12.formsite.com/HiRez/form48/secure_index.html "Form access to Hi-Rez API") to Hi-Rez Studios API.

## Installation
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/luissilva1044894/FlaskPyrezAPI/tree/master)

### Deploy (Heroku)
1. Go to [Heroku](https://id.heroku.com/login) and create a new app (eg: `your-app-name`)
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. `heroku login`
4. `git init`
5. `heroku git:remote -a your-app-name`
6. Download this repo and copy all files into `your-app-name` folder
7. Edit [`.env`](https://github.com/luissilva1044894/FlaskPyrezAPI/blob/master/.env) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [Hi-Rez Studios](https://fs12.formsite.com/HiRez/form48/secure_index.html).
8. `heroku config:push`
9. `git add .`
10. `git commit -m "Going to Heroku"`
11. `git push heroku master`
12. `heroku open` and a window will open with your app online
