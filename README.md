# FlaskPyrezAPI
A Paladins API endpoint for Twitch commands

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/luissilva1044894/FlaskPyrezAPI/tree/master)

## Deploy (Heroku)
1. Go to [Heroku](https://heroku.com/login) and create a new app (eg: `your-app-name`)
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
