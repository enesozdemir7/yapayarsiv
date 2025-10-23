from django import forms

from .models import ( Post, News, ForumCategory, Contact,
                    ForumSubCategory, ForumThread, ForumComment )

class ContactCreationForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ("contact_id", "email", "name_surname", "title", "body")

class ContactChangeForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ("contact_id", "email", "name_surname", "title", "body")

class ForumCategoryCreationForm(forms.ModelForm):

    class Meta:
        model = ForumCategory
        fields = ("category_id", "category", "explanation", "visible")

class ForumCategoryChangeForm(forms.ModelForm):

    class Meta:
        model = ForumCategory
        fields = ("category_id", "category", "explanation", "visible")


class ForumSubCategoryCreationForm(forms.ModelForm):

    class Meta:
        model = ForumSubCategory
        fields = ("subcategory_id", "category", "subcategory_name", "subcategory_explanation", "visible")


class ForumSubCategoryChangeForm(forms.ModelForm):

    class Meta:
        model = ForumSubCategory
        fields = ("subcategory_id", "category", "subcategory_name", "subcategory_explanation", "visible")


class ForumThreadCreationForm(forms.ModelForm):

    class Meta:
        model = ForumThread
        fields = ("thread_id", "title", "body", "category", "subcategory", "user", "visible", "reported")


class ForumThreadChangeForm(forms.ModelForm):

    class Meta:
        model = ForumThread
        fields = ("thread_id", "title", "body", "category", "subcategory", "user", "visible", "reported")

class ForumCommentForm(forms.ModelForm):

    class Meta:
        model = ForumComment
        fields = ("thread_id", "body", "user")

class ForumCommentCreationForm(forms.ModelForm):

    class Meta:
        model = ForumComment
        fields = ("comment_id", "thread_id", "body", "user", "visible", "reported")

class ForumCommentChangeForm(forms.ModelForm):

    class Meta:
        model = ForumComment
        fields = ("comment_id", "thread_id", "body", "user", "visible", "reported")


class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("thumbnail", "title","url","no","visible")

class PostChangeForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("thumbnail", "title", "url","no", "visible")

class NewsCreationForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ("news_id","banner", "title","body","desc", "sponsored", "visible")

class NewsChangeForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ("news_id","banner", "title","body","desc", "sponsored", "visible")
