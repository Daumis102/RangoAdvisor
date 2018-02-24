from django import forms
#from advisor.models import UserProfile
from django.contrib.auth.models import User

'''
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.",
                           label="Category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An Inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ("name",)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # what fields do we want to include in our form?
        # This way we dont need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them.
        # Here, we are hidding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ("category",)
        # or specify the fields to include
        # fields = ("title", "url", "views")

        def clean(self):
            cleaned_data = self.cleaned_data
            url = cleaned_data.get("url")

            # if url is not empty and doesnt start with http://
            # then prepend http://

            if url and not url.startwith("http://"):
                url = "http://"+ url
                cleaned_data["url"] = url

                return cleaned_data
'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)
'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
'''
