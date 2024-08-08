from flask import Flask, redirect, render_template, request
from flask import current_app as app
from application.models import *
from datetime import *


@app.route('/userlogin', methods=['GET','POST'])
def user_login():
  if request.method == "POST":
    u_mail = request.form.get('u_mail')
    u_pwd = request.form.get('u_pwd')
    this_user = User.query.filter_by(email = u_mail).first()
    if (this_user and this_user.type == 'general'):
      if this_user.password == u_pwd:
        u_name = User.query.filter_by(email = u_mail).first().name
        return redirect(f'/user/{this_user.u_id}')
      else:
        return 'Incorrect password'
    else:
      return 'User does not exist. An admin? Try admin login'
  return render_template('login_u.html')

@app.route('/register', methods=['GET','POST'])
def user_register():
  if request.method == "POST":
    u_name = request.form.get('u_name')
    u_mail = request.form.get('u_mail')
    u_pwd = request.form.get('u_pwd')
    this_user = User.query.filter_by(email = u_mail).first()
    if this_user:
      return "user already exist"
    else:
      new_user = User(email = u_mail, password = u_pwd, name = u_name)
      db.session.add(new_user)
      db.session.commit()
      return redirect('/userlogin')

  return render_template('register.html')



@app.route('/user/<int:u_id>', methods=['GET', 'POST'])
def user_dashboard(u_id):
  user = User.query.get(u_id)
  req_issues = Issues.query.filter_by(user_id=u_id, user_status='requested').all()
  issued = Issues.query.filter_by(user_id=u_id, user_status='approved').all()
  books = Books.query.all()
  return render_template('user_dash.html', user=user, req_issues = req_issues, books = books, issued=issued)

@app.route('/user/<int:u_id>/new_request/<int:b_id>', methods=['GET', 'POST'])
def new_req(u_id, b_id):
  user = User.query.get(u_id)
  book = Books.query.filter_by(b_id = b_id).first()

  if request.method == 'POST':
    user_requests_count = Issues.query.filter_by(user_id=u_id, user_status='requested').count()
    if user_requests_count == 5:
      return 'You have already requested the maximum number of books'
    elif Issues.query.filter_by(book_id=b_id, user_id=u_id, user_status='approved').first():
      return 'Book already issued'
    elif Issues.query.filter_by(book_id=b_id, user_id=u_id).first():
      return 'Book already requested'
    else:
      new_issue = Issues(book_id=b_id, user_id=u_id)
      db.session.add(new_issue)
      db.session.commit()

  return redirect(f'/user/{u_id}')

@app.route('/user/<int:u_id>/view/<int:b_id>', methods=['GET', 'POST'])
def viewbook(u_id, b_id):
  book = Books.query.filter_by(b_id = b_id).first()

  if request.method == 'POST':
    issue = Issues.query.filter_by(user_id=u_id, book_id=b_id, user_status='approved').first()
    if issue:
      issued_date_str = issue.issued_on
      issued_date = datetime.strptime(issued_date_str, '%d %b %y').date()
      days_since_issue = (date.today() - issued_date).days
      if days_since_issue > 7:
        return 'Cannot view books anymore, exceeded 7 day duration'
      else:
        return redirect(book.link)
  return redirect(f'/user/{u_id}')

@app.route('/user/<int:u_id>/return/<int:b_id>', methods=['GET', 'POST'])
def returnbook(u_id, b_id):

  if request.method == 'POST':
    issue = Issues.query.filter_by(user_id=u_id, book_id=b_id, user_status='approved').first()
    if issue:
      db.session.delete(issue)
      db.session.commit()
    else:
      return 'No approved issue found for this user and book'
      
  return redirect(f'/user/{u_id}')


##------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------
## Modules for Admin

@app.route('/adminlogin', methods=['GET','POST'])
def librarian_login():
  if request.method == "POST":
    u_mail = request.form.get('u_mail')
    u_pwd = request.form.get('u_pwd')
    this_user = User.query.filter_by(email = u_mail).first()
    if (this_user and this_user.type == 'admin'):
      if this_user.password == u_pwd:
        u_name = User.query.filter_by(email = u_mail).first().name
        return redirect('/admin')
      else:
        return 'Incorrect password'
    else:
      return 'User does not exist. Not an admin? Try user login'
  return render_template('login_l.html')

@app.route('/admin', methods=['GET', 'POST'])
def viewsection():
  sections = Section.query.all()
  requests = Issues.query.filter_by(lib_status="pending").all()
  return render_template('admin_dash.html', sections=sections, requests=requests)

@app.route('/admin/books/<string:s_name>', methods=['GET', 'POST'])
def viewbooks(s_name):
  books = Books.query.filter_by(b_section=s_name).all()
  return render_template('admin_dash_books.html', books=books)


@app.route('/admin/books/<string:s_name>/return/<string:b_title>', methods=['GET', 'POST'])
def removebook(s_name, b_title):
  if request.method == 'POST':
    book = Books.query.filter_by(b_section=s_name, b_title=b_title).first()
    if book:
      db.session.delete(book)
      db.session.commit()
    else:
      return 'Book Not Found'
      
  return redirect(f'/admin/books/{s_name}')


@app.route('/addbook/<string:s_name>', methods=['GET', 'POST'])
def addbooks(s_name):
  section = Section.query.filter_by(s_name=s_name).first()
  if request.method=='POST':
    b_title = request.form.get('b_title')
    b_author = request.form.get('b_author')
    b_link = request.form.get('b_link')
    b_section = s_name

    new_book = Books(b_title=b_title, b_author=b_author, b_section=b_section, link=b_link)
    db.session.add(new_book)
    db.session.commit()
    return redirect(f'/admin/books/{s_name}')

  return render_template('add_book.html', b_section=s_name, section=section)

@app.route('/editbook/<string:s_name>/<int:b_id>', methods=['GET', 'POST'])
def editbooks(s_name, b_id):
  section = Section.query.filter_by(s_name=s_name).first()
  book = Books.query.filter_by(b_id=b_id).first()
  if request.method=='POST':
    b_title = request.form.get('b_title')
    b_author = request.form.get('b_author')
    b_link = request.form.get('b_link')
    b_section = request.form.get('b_section')

    book.b_title = b_title
    book.b_author = b_author
    book.link = b_link
    book.b_section = b_section
    db.session.commit()
    return redirect(f'/admin/books/{s_name}')

  return render_template('edit_book.html', b_section=s_name, section=section, book=book)


@app.route('/addsection', methods=['GET', 'POST'])
def addsection():
  date_today = date.today()
  s_date = date_today.strftime('%d %b %y')
  if request.method=='POST':
    s_name = request.form.get('s_name')
    
    print(s_date)
    description = request.form.get('description')

    new_section = Section(s_name=s_name, s_date=s_date, description=description)
    db.session.add(new_section)
    db.session.commit()
    return redirect(f'/admin')

  return render_template('add_section.html', s_date=s_date)

@app.route('/admin/reject/<int:book_id>/<int:user_id>', methods=['GET','POST'])
def reject_req(book_id, user_id):
  if request.method=='POST':
    issue = Issues.query.filter_by(user_id=user_id, book_id=book_id, user_status='requested').first()
    if issue:
      db.session.delete(issue)
      db.session.commit()
    else:
      return 'No requests found for this user and book'
      
  return redirect(f'/admin')

@app.route('/admin/grant/<int:book_id>/<int:user_id>', methods=['GET','POST'])
def grant_req(book_id, user_id):
  date_today = date.today()
  final_date = date_today.strftime('%d %b %y')
  if request.method=='POST':
    issue = Issues.query.filter_by(user_id=user_id, book_id=book_id, user_status='requested').first()
    if issue:
      issue.user_status = "approved"
      issue.lib_status = "approved"
      issue.issued_on = final_date
      db.session.commit()
    else:
      return 'No requests found for this user and book'
      
  return redirect(f'/admin')

@app.route('/admin/allissues', methods=['GET', 'POST'])
def allissues():
  issues = Issues.query.all()
  return render_template('admin_dash_issues.html', issues=issues)

@app.route('/admin/allissues/revoke/<int:book_id>/<int:user_id>', methods=['GET','POST'])
def revoke_access(book_id, user_id):
  if request.method=='POST':
    issue = Issues.query.filter_by(user_id=user_id, book_id=book_id, user_status='approved').first()
    if issue:
      db.session.delete(issue)
      db.session.commit()
    else:
      return 'No requests found for this user and book'
      
  return redirect(f'/admin/allissues')