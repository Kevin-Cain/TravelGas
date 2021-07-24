from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    return render_template('base.html')


@views.route('/Trip', methods=['GET','POST'])
def Trip():
    if request.method == 'POST':
        MPG = request.form.get("MPG") 
        GasTankCapacity = request.form.get("GasTankCapacity")
        HomeAddress = request.form.get("Origin")
        Destination = request.form.get("Destination")

    return render_template('trip.html')