from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#database configuration
app = Flask(__name__) #application instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTasks.db' #creates db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app) #database instance
class TaskList(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String[50])
    section = db.Column(db.String(20), nullable=False) 

# Create tables in DB
with app.app_context():
    db.create_all()


# 3 routes listed below
@app.route('/') #
def home():
    #  Get all tasks for each section from the database
    today_tasks = TaskList.query.filter_by(section='Today').all()
    tomorrow_tasks = TaskList.query.filter_by(section='Tomorrow').all()
    upcoming_tasks = TaskList.query.filter_by(section='Upcoming').all()

    # Send the task lists to the HTML template (index.html)
    # So we can loop through them and display in the correct boxes
    return render_template('index.html',
                           today_tasks=today_tasks,
                           tomorrow_tasks=tomorrow_tasks,
                           upcoming_tasks=upcoming_tasks)
     
     
@app.route('/add', methods=['POST'])
def add():
    content = request.form['entry']         # Get entry from form(task submission referred to as entry on index.html)
    section = request.form.get('section')   # Get the section (e.g., Today)

    if not section:
        return "Missing section", 400       # Optional: Guard against missing input

    new_task = TaskList(name=content, section=section) #db module named Tasklist
    db.session.add(new_task)                           # adding entry to db in form of (TaskList(task1, today))
    db.session.commit()
    return redirect(url_for('home'))
    

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task = TaskList.query.get_or_404(task_id)  # Find task by ID or return 404
    db.session.delete(task)                    # Delete it from DB
    db.session.commit()                        # Save changes
    return redirect(url_for('home'))           # Go back to main page

if __name__ == '__main__': # This ensures the app runs only if this file is executed directly
    app.run(debug=True)     # Starts the Flask development server with debug mode enabled
   

