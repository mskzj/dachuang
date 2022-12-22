from django import forms
from django.core.validators import RegexValidator
from .models import Room
from ckeditor.widgets import CKEditorWidget

class Roomform(forms.Form):
    room_name = forms.CharField(
        max_length=20,
        min_length=1,
        label="聊天室名称",
        error_messages={
            'required':'请输入名称',
            'max_length':'最大长度不能超过十个字节',
        }
    )
    room_type = forms.CharField(
        max_length=20,
        min_length=0,
        label="聊天室描述",
        error_messages={
            'max_length':'最大长度不能超过20个字节',
        }
    )