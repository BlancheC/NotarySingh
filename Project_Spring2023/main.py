# Author: Blanche Chung
# Created Date: Spring 2023
# Description: This file is the main file for the website package. It creates the flask app and the database.

from website import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)