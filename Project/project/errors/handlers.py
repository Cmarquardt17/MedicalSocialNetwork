from flask import Blueprint, render_template

#This creates a "Blueprint" that all pages will use in case of an error
errors = Blueprint('errors', __name__)

#All of the possible errors for each webpage
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
