poetry run pip freeze > requirements.txt
git commit requirements.txt -m "update requirements.txt"
git push heroku main
