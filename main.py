
from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog1:beproductive@localhost:8889/build-a-blog1'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        

    def is_valid(self):
        
        if self.title and self.body :
            return True
        else:
            return False

@app.route("/")
def index():
    return redirect("/blog")
    

@app.route("/blog")
def display_blog():
   
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('blog.html', title="Blog Entry", entry=entry)
    else:   
        all_entries = Blog.query.all()   
    return render_template('base.html', title="All Entries", all_entries=all_entries)

#
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_entry = Blog(new_title, new_body)
        
        if (new_title == "") or (new_body == "") :
            title_error="please fill the title"
            body_error="please fill the body"
            return render_template('newpost.html',
                title="Create new blog entry",
                new_title=new_title,
                new_body=new_body, title_error=title_error,body_error=body_error)

        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()

            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
        else:
            return render_template('newpost.html',
                new_title=new_title,
                new_body=new_body)

    else: 
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
