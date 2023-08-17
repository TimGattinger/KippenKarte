import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///markers.db'
db = SQLAlchemy(app)

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(100), nullable=False)

db.create_all()

@app.route('/')
def map():
    markers = Marker.query.all()
    return render_template('map.html', markers=markers)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    lat = request.form['lat']
    lon = request.form['lon']
    label = request.form['label']

    new_marker = Marker(lat=lat, lon=lon, label=label)
    db.session.add(new_marker)
    db.session.commit()

    return redirect('/')

@app.route('/delete_marker/<int:marker_id>', methods=['POST'])
def delete_marker(marker_id):
    marker = Marker.query.get_or_404(marker_id)
    db.session.delete(marker)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # Use the PORT environment variable provided by Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


