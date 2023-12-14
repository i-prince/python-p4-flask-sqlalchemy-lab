#!/usr/bin/env python3

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    species = db.Column(db.String(255), nullable=False)
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeeper.id'), nullable=False)
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosure.id'), nullable=False)

    def __repr__(self):
        return f'<Animal {self.name}>'


class Zookeeper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    animals = db.relationship('Animal', backref='zookeeper', lazy=True)

    def __repr__(self):
        return f'<Zookeeper {self.name}>'


class Enclosure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(255), nullable=False)
    open_to_visitors = db.Column(db.Boolean, default=True)
    animals = db.relationship('Animal', backref='enclosure', lazy=True)

    def __repr__(self):
        return f'<Enclosure {self.id}>'


@app.route('/')
def home():
    return '<h1>Zoo app</h1>'


@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    return render_template('animal.html', animal=animal)


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    return render_template('zookeeper.html', zookeeper=zookeeper)


@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    return render_template('enclosure.html', enclosure=enclosure)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
