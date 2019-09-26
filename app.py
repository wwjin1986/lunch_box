from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/lunch_box'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lunchbox'

db = SQLAlchemy(app)


class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    score = db.Column(db.Integer)

    def __init__(self, name, category, score):
        self.name = name
        self.category = category
        self.score = score

    def __repr__(self):
        return f"{self.id}---{self.name}"


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        foods = db.session.query(Foods).all()
        return render_template("index.html", foods=foods)
    else:
        form_food = request.form['food']
        form_category = request.form['category']
        form_score = request.form['score']
        new_food = Foods(name=form_food, category=form_category, score=form_score)
        try:
            db.session.add(new_food)
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return str(ex)


@app.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    food_to_delete = Foods.query.get_or_404(id)
    try:
        db.session.delete(food_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as ex:
        return str(ex)


if __name__ == "__main__":
    app.run(debug=True)
