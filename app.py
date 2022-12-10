"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
import os
from dotenv import load_dotenv
import requests

load_dotenv()

PETFINDER_API_SECRET = os.environ['PETFINDER_API_SECRET']
PETFINDER_API_KEY = os.environ['PETFINDER_API_KEY']

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get('/')
def show_homepage():
    '''Show the homepage'''

    pets = Pet.query.all()

    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    '''Pet add form; handle adding'''

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes)

        db.session.add(pet)
        db.session.commit()

        flash(f'{name} added!')
        return redirect('/')

    else:
        return render_template('add_pet.html', form=form)

@app.route("/<int:petid>", methods=["GET", "POST"])
def edit_pet(petid):
    """ displays pet details and form to edit pet """

    pet = Pet.query.get_or_404(petid)
    form = EditPetForm(obj=pet)


    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        flash(f'{pet.name} edited!')
        return redirect(f"/{petid}")

    else:
        return render_template('pet_details.html', form = form, pet = pet)
