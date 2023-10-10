from django import forms


#csv file upload
class UploadForm(forms.Form):
    uploadfile = forms.FileField()