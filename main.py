from app import app,db
import admin
from models import *
import views
from flask import url_for, request
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin
from entries.blueprint import entries
app.register_blueprint(entries, url_prefix = '/entries')

@app.route('/latest.atom')
def recent_feed():
    feed = AtomFeed(
    'Latest Blog Post',
    feed_url = request.url,
    url = request.url_root,
    author = request.url_root
    )
    entries = Entry.query.filter(Entry.status == Entry.public).order_by(Entry.created_timestamp).limit(15).all()

    for entry in entries:
        feed.add(

        entry.title,
        entry.body,
        author= entry.author,
        content_type='html',
        id = entry.id,
        url = urljoin(request.url_root,url_for('entries.detail', slug = entry.slug)),
        updated = entry.modified_timestamp,
        published = entry.created_timestamp
        )

    return feed.get_response()

if __name__=='__main__':
    app.run()
