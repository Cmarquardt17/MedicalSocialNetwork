from project import create_app

#This initializes the app in it's entirety
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
