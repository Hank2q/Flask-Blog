from flaskblog import create_app

app = create_app()

# * use this to run the script directly instead of > flask run
if __name__ == "__main__":
    app.run(debug=True)
