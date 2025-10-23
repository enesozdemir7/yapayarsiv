from rest_framework import serializers
from .models import Help,HelpComments,Blog,BlogComments,Course,NotificationsUsers
from django.utils.timesince import timesince

class HelpCommentsSerializer(serializers.ModelSerializer):
    
    time_since = serializers.SerializerMethodField()
    creator_username = serializers.SerializerMethodField()
    creator_fullname = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    sub_comments = serializers.SerializerMethodField()

    class Meta:
        model = HelpComments
        fields = '__all__'


    def get_time_since(self, obj):
        return timesince(obj.date) + ", " + 'önce'
    
    def get_creator_username(self, obj):
        return obj.user.username
    
    def get_creator_fullname(self, obj):
        return obj.user.full_name()
    
    def get_profile_pic(self, obj):
        if obj.user.profile_pic:

            return str(obj.user.profile_pic.url)
        else:
            return ''
    
    def get_sub_comments(self,obj):

        return HelpComments.objects.filter(parent=obj.id).count()
        

class BlogCommentsSerializer(serializers.ModelSerializer):
    
    time_since = serializers.SerializerMethodField()
    creator_username = serializers.SerializerMethodField()
    creator_fullname = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    sub_comments = serializers.SerializerMethodField()

    class Meta: 
        model = BlogComments
        fields = '__all__'


    def get_time_since(self, obj):
        return timesince(obj.date) + ", " + 'önce'
    
    def get_creator_username(self, obj):
        return obj.user.username
    
    def get_creator_fullname(self, obj):
        return obj.user.full_name()
    
    def get_profile_pic(self, obj):
        if obj.user.profile_pic:

            return str(obj.user.profile_pic.url)
        else:
            return ''
    
    def get_sub_comments(self,obj):

        return BlogComments.objects.filter(parent=obj.id).count()

class HelpSerializer(serializers.ModelSerializer):

    time_since = serializers.SerializerMethodField()
    creator_username = serializers.SerializerMethodField()
    creator_fullname = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    help_comments = serializers.SerializerMethodField()

    class Meta:
        model = Help
        fields = '__all__'


    def get_time_since(self, obj):
        return timesince(obj.date) + ", " + 'önce'
    
    def get_creator_username(self, obj):
        return obj.user.username
    
    def get_creator_fullname(self, obj):
        return obj.user.full_name()
    
    def get_profile_pic(self, obj):
        if obj.user.profile_pic:

            return str(obj.user.profile_pic.url)
        else:
            return ''
        
    def get_help_comments(self, obj):
        return HelpComments.objects.filter(help=obj.id).count()
    

class BlogSerializer(serializers.ModelSerializer):
    
    time_since = serializers.SerializerMethodField()
    creator_username = serializers.SerializerMethodField()
    creator_fullname = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    blog_comments = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'


    def get_time_since(self, obj):
        return timesince(obj.created_at) + ", " + 'önce'
    
    def get_creator_username(self, obj):
        return obj.author.username
    
    def get_creator_fullname(self, obj):
        return obj.author.full_name()
    def get_category(self,obj):
        return list(obj.category.all().values_list('slug','name'))
    def get_profile_pic(self, obj):
        if obj.author.profile_pic:

            return str(obj.author.profile_pic.url)
        else:
            return ''
        
    def get_blog_comments(self, obj):
        return BlogComments.objects.filter(blog=obj.id).count()



class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return obj.get_lesson_count()
    

class NotificationsSerializer(serializers.ModelSerializer):
    time_since = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = NotificationsUsers
        fields = '__all__'


    def get_time_since(self, obj):
        return timesince(obj.notification.date) + ", " + 'önce'

    def get_title(self, obj):
        return obj.notification.title

    def get_link(self, obj):
        return obj.notification.link

    def get_sender(self, obj):
        return obj.notification.sender