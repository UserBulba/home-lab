# Build Flask app on Heroku

Create Procfile file.

```bash
echo "web: gunicorn app:app" > Procfile
```

Initializes the Heroku application.

```bash
heroku login
heroku create vagrant-app
heroku git:clone -a vagrant-app
git add .
git commit -am "Initial commit"
git push heroku master
```

```bash
heroku buildpacks:set heroku/python
```

```bash
#
heroku pipelines:create --app vagrant-app --stage production vagrant-app
#
heroku git:remote --app vagrant-app --remote prod


#
heroku create vagrant-app-staging --remote staging
#
heroku pipelines:add vagrant-app --app vagrant-app-staging --stage staging
#
git push staging master


#
heroku create vagrant-app-development --remote development
#
heroku pipelines:add vagrant-app --app vagrant-app-development --stage development
#
git push development master


#
heroku pipelines:promote --remote development
#
heroku pipelines:promote --remote staging
```

```bash
git add.
git commit -am "Change made"
vagrant push
```
