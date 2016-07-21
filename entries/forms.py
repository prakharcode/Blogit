import wtforms
from wtforms.validators import DataRequired,Email,Optional,URL,Length
from models import Entry, Tag



class ImageForm(wtforms.Form):
    file = wtforms.FileField('Image file',validators = [DataRequired()])



class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            return ','.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        new_names = set(tag_names)- set([tag.name for tag in existing_tags])
        new_tags = [Tag(name = name) for name in new_names]
        return new_tags + list(existing_tags)

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data=[]



class EntryForm(wtforms.Form):
    title = wtforms.StringField('Title', validators = [DataRequired()])
    body = wtforms.TextAreaField('Body', validators = [DataRequired()])
    status = wtforms.SelectField('Entry Status', choices=((1,'POST'),
    (0,'DRAFT')), coerce=int)
    tags = TagField('Tags', description='Separate multiple tags with commas.')
    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generator_slug()
        return entry
