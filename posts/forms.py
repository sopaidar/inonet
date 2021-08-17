import uuid
from django.forms import Form, CharField, BooleanField, FileField
from django.utils.translation import gettext_lazy as _

class PostCreationFormForm(Form):
    
    text = CharField(label=_("text"), required=True, max_length=511)
    image = FileField(label=_("image"), required=False)
    shared_post = CharField(label=_("shared_post"), required=False)
    draft = BooleanField(label=_("draft"), required=False)

        