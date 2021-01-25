poetry run pip freeze > requirements.txt
git commit -m "update requirements.txt" requirements.txt 
git push heroku main
