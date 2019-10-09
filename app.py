from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, func

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
    food = db.Column(db.String(200), nullable=True)
    score = db.Column(db.Integer)

    def __init__(self, name, food, score):
        self.name = name
        self.food = food
        self.score = score

    def __repr__(self):
        return f"{self.name} {self.food} "


db.create_all()
db.session.commit()


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        foods = db.session.query(Foods).all()
        plans = db.session.query(func.min(Plans.id).label('id'), Plans.name,
                                 func.group_concat(Plans.food.distinct()).label('foods'),
                                 Plans.score).group_by(Plans.name)
        return render_template("index.html", foods=foods, plans=plans)
    else:
        form_food = request.form['food']
        form_category = request.form['category']
        form_score = request.form['score']
        new_food = Foods(
            name=form_food, category=form_category, score=form_score)
        try:
            db.session.add(new_food)
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return str(ex)


@app.route("/foods/<int:id>", methods=['GET', 'POST'])
def delete_food(id):
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


@app.route("/plans/add", methods=['GET', 'POST'])
def add_plan():
    if request.method == 'GET':
        return redirect('/')
    else:
        plan = request.json
        plan_name = plan['planName']
        score = plan['score']
        for food in plan['selectedFoods']:
            new_plan = Plans(name=plan_name, food=food, score=score)
            try:
                db.session.add(new_plan)
                db.session.commit()
            except Exception as ex:
                return str(ex)
        return redirect('/')


@app.route("/plans/<string:name>", methods=['GET', 'POST'])
def delete(name):
    if request.method == 'GET':
        return redirect('/')
    else:
        plans_to_delete = Plans.query.filter_by(name=name).all()
        print(plans_to_delete)
        for plan in plans_to_delete:
            try:
                db.session.delete(plan)
                db.session.commit()
            except Exception as ex:
                return str(ex)
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
