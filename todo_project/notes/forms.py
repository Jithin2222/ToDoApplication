from django import forms
from .models import Note, Folder

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Folder name'
            }),
            'color': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'folder', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control note-title-input',
                'placeholder': 'Note title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control note-content-input',
                'placeholder': 'Write your note here...',
                'rows': 10
            }),
            'folder': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(user=user)
        self.fields['folder'].required = False