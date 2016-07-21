from app import app, db
from flask import Blueprint, flash, render_template, request, redirect, url_for, g
from models import Entry,Tag,entry_tags,User
from helper import object_list
from forms import EntryForm, ImageForm
import os
from flask_login import login_required
from werkzeug import secure_filename

entries = Blueprint('entries', __name__, template_folder = 'templates')

def get_entry_or_404(slug, author = None):
    query = Entry.query.filter( Entry.slug == slug)
    if author:
        query = query.filter(Entry.author == author)
    else:
        query = filter_status_by_user(query)
    return query.first_or_404()

def filter_status_by_user(query):
    if not g.user.is_authenticated:
        query = query.filter(Entry.status == Entry.public)
    else:
        query = query.filter((Entry.status == Entry.public) |((Entry.author == g.user) & (Entry.status != Entry.eleted)))
    return query



@entries.route('/image-upload/', methods = ['GET','POST'])
@login_required
def image_upload():
    if request.method == 'POST':
        form = ImageForm(request.form)
        if form.validate():
            image_file = request.files['file']
            filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
            image_file.save(filename)
            flash('Saved %s' %os.path.basename(filename),'success')
            return redirect(url_for('entries.index'))
    else:
            form = ImageForm()
    return render_template('entries/image_upload.html', form = form )



@entries.route('/')
@login_required
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc()).filter(Entry.status!='2')
    return entry_list('entries/index.html',entries)

@entries.route('/create/', methods = ['GET','POST'])
@login_required
def create():
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry(author = g.user))
            db.session.add(entry)
            db.session.commit()
            flash('Blog: %s ,Created! ' %entry.title, 'success')
            return redirect(url_for('entries.detail', slug = entry.slug))
        else:
            form = EntryForm()
    return render_template('entries/create.html',form = form)



@entries.route('/<slug>/edit/', methods =['GET','POST'])
@login_required
def edit(slug):
    entry = get_entry_or_404(slug, g.user)
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            flash('Blog: %s ,Edited! ' %entry.title, 'success')
            return redirect(url_for('entries.detail', slug = entry.slug))
    else:
        form = EntryForm(obj = entry)
        return render_template('entries/edit.html', entry = entry, form = form)


@entries.route('/<slug>/delete/', methods = ['GET', 'POST'])
@login_required
def delete(slug):
    entry = get_entry_or_404(slug, g.user)
    if request.method == 'POST':
        entry.status = 2
        db.session.add(entry)
        db.session.commit()
        flash('Blog: %s ,Deleted! ' %entry.title, 'success')
        return redirect(url_for('entries.index'))
    return render_template('entries/delete.html',entry = entry )

@entries.route('/tags/')
def tag_index():
    tags = Tag.query.join(entry_tags)
    return entry_list('entries/tag_index.html',tags)

@entries.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.order_by(Tag.name).filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return object_list('entries/tag_detail.html', entries,name = tag.name)

@entries.route('/<slug>')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    username = User.query.filter(Entry.id == entry.id, Entry.author_id==User.id).all()[0].name
    return render_template('entries/detail.html', entry = entry, username = username)

def entry_list(template, query, **context):
    search = request.args.get('q')
    if search:
        query=query.filter(Entry.body.contains(search) | (Entry.title.contains(search)))
    return object_list(template, query,**context)
