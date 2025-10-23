from django import forms

from .models import Tool, ToolStars, ToolFavoritedUsers



class ToolStarsForm(forms.ModelForm):

    class Meta:
        model = ToolStars
        fields = (
            "user", "tool", "star"
            )


class ToolCreationForm(forms.ModelForm):

    class Meta:
        model = Tool
        fields = (
            "tool_name", "title", "banner", "body",
            "subcategory", "fee", "product_url", "is_priority",
            "sponsored", "visible", 
            )

class ToolChangeForm(forms.ModelForm):

    class Meta:
        model = Tool
        fields = (
            "tool_name", "title", "banner", "body",
            "subcategory", "fee", "product_url", "is_priority",
            "sponsored", "visible", 
            )
