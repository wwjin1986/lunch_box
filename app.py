from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b4afdf249e41b5:2df06650@us-cdbr-iron-east-02.cleardb.net/heroku_9e117b96381e622'

db = SQLAlchemy(app)


class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    score = db.Column(db.Integer)

    def __init__(self, name, category, score):
        self.name = name
        self.category = category
        self.score = score

    def __repr__(self):
        return f"{self.name} {self.category} {self.score}"


class Plans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    foods = db.Column(db.JSON, nullable=False)

    def __init__(self, name, foods):
        self.name = name;
        self.foods = foods;

    def __repr__(self):
        return f"{self.name} {self.foods} "


db.create_all()
db.session.commit()


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


@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    food_to_delete = Foods.query.get_or_404(id)
    try:
        db.session.delete(food_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as ex:
        return str(ex)


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    food = Foods.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("edit.html", food=food)
    elif request.method == 'POST':
        food.name = request.form['name']
        food.category = request.form['category']
        food.score = request.form['score']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return str(ex)


@app.route("/add-plan", methods=['GET', 'POST'])
def add_plan():
    if request.method == 'GET':
        foods = db.session.query(Foods).all()
        return render_template("index.html", foods=foods)
    else:
        plan_name = request.form['plan-name']
        form_foods = request.form['category']

        new_food = Foods(name=form_food, category=form_category, score=form_score)
        try:
            db.session.add(new_food)
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return str(ex)


if __name__ == "__main__":
    app.run(debug=True)
