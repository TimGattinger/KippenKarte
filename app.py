from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import folium

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///markers.db'
db = SQLAlchemy(app)

# Create a base map centered around Kiel
kiel_coords = [54.323293, 10.122765]

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(255), nullable=False)

def create_sample_data():
    db.create_all()

    # Add sample markers
    sample_markers = [
        Marker(lat=54.323293, lon=10.122765, label="Kiel"),
        Marker(lat=54.314, lon=10.127, label="Marker 1"),
        Marker(lat=54.320, lon=10.130, label="Marker 2"),
    ]

    for marker in sample_markers:
        db.session.add(marker)

    db.session.commit()

@app.route('/')
def index():
    markers = Marker.query.all()
    return render_template('map.html', markers=markers)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])
    label = request.form['label']
    marker = Marker(lat=lat, lon=lon, label=label)
    db.session.add(marker)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        create_sample_data()
    app.run(debug=True)


