from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#setup application (name references this file?):
app = Flask(__name__)

#tells the app where the database is located, here we are using sqlite (4 forward slashes is an absolute path, 3 is a relative path (e.g., the project location))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#initialize the database
db = SQLAlchemy(app)

#make a model
class Todo(db.Model):
    #primary_key identifer is always unique, it will never have a duplicate
    id = db.Column(db.Integer, primary_key=True)
    #200 character limit, nullable false means, you can't leave it blank
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # return Task + the task that is created
        return '<Task %r>' % self.id

#create index route:

# route can accept post and get methods (get is the default)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # from index.html:     <div class="form">
        #                       <form action="/" method="POST">
        #                           <input type="text" name="content" id="content">
        #                           <input type="submit" value="Add Task">
        #                       </form>
        #                    </div> 
        # as you can see, 'content' below matches the input "name" above:
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try: 
            db.session.add(new_task)
            db.session.commit()
            # return a redirect back to the index
            return redirect('/')
        except:
            return "There was an issue adding your task 👾"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            # don't need a db.session.add, instead here you grab the content from the form and update it.
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the task"

    else:
        return render_template('update.html', task=task)

#define function for the route:

def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

































# from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'

#     else:
#         return render_template('update.html', task=task)


# if __name__ == "__main__":
#     app.run(debug=True)
