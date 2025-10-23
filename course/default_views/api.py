from course.models import Help,HelpComments,Blog,BlogComments,Category,Course,FAQ,NotificationsUsers,Notifications,UserBlogLikes,UserHelpLikes,UserBlogCommentLikes,UserHelpCommentLikes
from course.serializers import HelpSerializer,HelpCommentsSerializer,BlogSerializer,BlogCommentsSerializer,CourseSerializer,NotificationsSerializer
from urllib.parse import parse_qs
import json
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from course.permissions import CustomPermission
from django.shortcuts import get_object_or_404

class CommentPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1

class NotificationCheckPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1

import logging

logger = logging.getLogger(__name__)

class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CustomPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        post_id = self.request.query_params.get('post_id', None)

        if search == '':
            search = None
        if post_id:
            queryset = queryset.filter(id=post_id)
        if search is not None:
            queryset = queryset.filter(Q(title__icontains=search) | Q(details__icontains=search))

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['post_likes'] = list(UserHelpLikes.objects.filter(user=request.user).values_list('post__id', flat=True))
        return response

    def create(self, request, *args, **kwargs):
        serializer = HelpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        else:
            # Hata mesajlarını logla
            logger.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class HelpCommentsViewSet(viewsets.ModelViewSet):
    queryset = HelpComments.objects.all()
    serializer_class = HelpCommentsSerializer
    pagination_class = CommentPagination
    permission_classes = [CustomPermission]


    def get_queryset(self):
        queryset = super().get_queryset()

        help_id = self.request.query_params.get('help_id', None)
        comment_id = self.request.query_params.get('comment_id', None)

        if help_id == '':
            help_id = None

        if comment_id == '':
            comment_id = None

        if help_id is not None:
            queryset = queryset.filter(help=help_id,parent=comment_id)

        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)

        response.data['comment_likes'] = list(UserHelpCommentLikes.objects.filter(user=request.user).values_list('comment__id',flat=True))

        return response

    def create(self, request, *args, **kwargs):
        serializer = HelpCommentsSerializer(data=request.data)

        if serializer.is_valid():
            s = serializer.save(user=request.user) 

            if s.parent:
                message = "Yorumuna yanıt verdi."
            else:
                message = "Paylaşımına yorum yaptı."
                
            n = Notifications.objects.create(title=message,sender=request.user.username,link='/yardim/?post_id={}'.format(s.help.id),system=False)
            NotificationsUsers.objects.create(user=s.help.user,notification=n)

            return Response({'status':'ok'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CustomPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('search', None)
        cat = self.request.query_params.get('cat', None)
        post_id = self.request.query_params.get('post_id', None)

        if cat:
            queryset = queryset.filter(category__slug__in=[cat])
        if post_id:
            queryset = queryset.filter(id=post_id)
            
        if search == '':
            search = None

        if search is not None:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['post_likes'] = list(UserBlogLikes.objects.filter(user=request.user).values_list('post__id',flat=True))

        return response

    def create(self, request, *args, **kwargs):

        get_cat_list = request.POST.getlist('cats',None)
        get_title = request.POST.get('title',None)
        get_content = request.POST.get('content',None)
        video_embed_link = request.POST.get('vimeo_embed_link',None)

        get_banner = request.FILES.get("banner",None)
        if get_cat_list and get_title and get_content:
            get_selected_cats = Category.objects.filter(id__in=get_cat_list)
            
            created_blog = Blog.objects.create(title=get_title,video_embed_link=video_embed_link,content=get_content,author=request.user,banner=get_banner)
            created_blog.category.add(*get_selected_cats)
            return Response({'status':'ok'}, status=status.HTTP_201_CREATED)
        else:
            if len(get_cat_list) == 0:
                return Response({'status':'error','message':'Lütfen kategori seçiniz.'}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'error','message':'Bilinmeyen bir hata oluştu.'}, status=status.HTTP_400_BAD_REQUEST)
    

class BlogCommentsViewSet(viewsets.ModelViewSet):
    queryset = BlogComments.objects.all()
    serializer_class = BlogCommentsSerializer
    pagination_class = CommentPagination
    permission_classes = [CustomPermission]


    def get_queryset(self):
        queryset = super().get_queryset()

        blog_id = self.request.query_params.get('blog_id', None)
        comment_id = self.request.query_params.get('comment_id', None)

        if blog_id == '':
            blog_id = None

        if comment_id == '':
            comment_id = None

        if blog_id is not None:
            queryset = queryset.filter(blog=blog_id,parent=comment_id)

        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)

        response.data['comment_likes'] = list(UserBlogCommentLikes.objects.filter(user=request.user).values_list('comment__id',flat=True))

        return response

    def create(self, request, *args, **kwargs):
        serializer = BlogCommentsSerializer(data=request.data)
        if serializer.is_valid():
            s = serializer.save(user=request.user)
            if s.parent:
                message = "Yorumuna yanıt verdi."
            else:
                message = "Paylaşımına yorum yaptı."
                
            n = Notifications.objects.create(title=message,sender=request.user.username,link='/hizli-ogren/?post_id={}'.format(s.blog.id),system=False)
            NotificationsUsers.objects.create(user=s.blog.author,notification=n)


            return Response({'status':'ok'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CustomPermission]


    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.query_params.get('query', None)
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(desc__icontains=query),active=True)

        return queryset

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = NotificationsUsers.objects.all()
    serializer_class = NotificationsSerializer
    pagination_class = NotificationCheckPagination
    permission_classes = [CustomPermission]


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        new_items = queryset.filter(showing=False,user=request.user).count()
        sound_status = '0' 
        if queryset.filter(showing=False,sound_status=False,user=request.user).count() > 0:
            for x in queryset.filter(showing=False,sound_status=False,user=request.user):
                x.sound_status = True
                x.save()
            sound_status = '1'
        
        queryset = queryset.filter(user=request.user)[0:4]
        serializer = self.get_serializer(queryset, many=True)


        return Response({'results': serializer.data, 'new_items':new_items ,'sound_status':sound_status})

class NotificationShowApiView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.course_user or request.user.is_superser:

                get_not_showings = NotificationsUsers.objects.filter(showing=False,user=request.user)
                for x in get_not_showings:
                    x.showing = True
                    x.sound_status = True
                    x.save()
                return Response({'status':'ok'},status=status.HTTP_200_OK)
            else:
                return Response({'status':'no'},status=status.HTTP_401_OK)

from rest_framework.decorators import api_view
from rest_framework.response import Response

from course.permissions import course_custom_permission

@api_view(['GET'])
@course_custom_permission('course')
def basedSearch(request):
    query = request.GET.get('query',None)
    if query:

        try:

            blog_results = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).count()
            help_results = Help.objects.filter(Q(title__icontains=query) | Q(details__icontains=query)).count()
            course_results = Course.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query),active=True).count()
            faq_results = FAQ.objects.filter(Q(question__icontains=query) | Q(reply__icontains=query)).count()

            results =  {
                'blog':blog_results,'blog_search_link':f'/hizli-ogren/?q={query}',
                'help':help_results,'help_search_link':f'/yardim/?q={query}',
                'course':course_results,'course_search_link':f'/kurslar/?query={query}',
                'faq':faq_results,'faq_search_link':f'/sss/?q={query}',
            }

            return Response(results,status=status.HTTP_200_OK)
        except:
            return Response({'status':'error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status':'error'},status=status.HTTP_403_FORBIDDEN)
    


@api_view(['GET'])
@course_custom_permission('course')
def blogLike(request):

    post_id = request.GET.get('post_id',None)
    if post_id:

        try:
            get_post = get_object_or_404(Blog,id=post_id)
            ubl = UserBlogLikes.objects.filter(user=request.user,post=get_post).last()

            results =  {
                'status':'no'
            }

            if ubl:
                ubl.delete()
                get_post.like_count -=1 
                get_post.save()
                results =  {
                    'status':'un-like',
                    'new_count':get_post.like_count,

                }
            else: 
                UserBlogLikes.objects.create(user=request.user,post=get_post)
                get_post.like_count +=1 
                get_post.save()

                n = Notifications.objects.create(title="Paylaşımını beğendi",sender=request.user.username,link='/hizli-ogren/?post_id={}'.format(post_id),system=False)
                NotificationsUsers.objects.create(user=request.user,notification=n)

                results =  {
                    'status':'like',
                    'new_count':get_post.like_count,
                }



            return Response(results,status=status.HTTP_200_OK)
        except:
            return Response({'status':'error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status':'error'},status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@course_custom_permission('course')
def blogCommentLike(request):

    comment_id = request.GET.get('comment_id',None)
    post_id = request.GET.get('post_id',None)
    if comment_id:

        try:
            get_comment = get_object_or_404(BlogComments,id=comment_id)
            ubl = UserBlogCommentLikes.objects.filter(user=request.user,comment=get_comment).last()

            results =  {
                'status':'no'
            }

            if ubl:
                ubl.delete()
                get_comment.like_count -=1 
                get_comment.save()
                results =  {
                    'status':'un-like',
                    'new_count':get_comment.like_count,

                }
            else: 
                UserBlogCommentLikes.objects.create(user=request.user,comment=get_comment)
                get_comment.like_count +=1 
                get_comment.save()

                n = Notifications.objects.create(title="Yorumunu beğendi",sender=request.user.username,link='/hizli-ogren/?post_id={}'.format(post_id),system=False)
                NotificationsUsers.objects.create(user=request.user,notification=n)

                results =  {
                    'status':'like',
                    'new_count':get_comment.like_count,
                }



            return Response(results,status=status.HTTP_200_OK)
        except:
            return Response({'status':'error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status':'error'},status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@course_custom_permission('course')
def helpLike(request):

    post_id = request.GET.get('post_id',None)
    if post_id:

        try:
            get_post = get_object_or_404(Help,id=post_id)
            ubl = UserHelpLikes.objects.filter(user=request.user,post=get_post).last()

            results =  {
                'status':'no'
            }

            if ubl:
                ubl.delete()
                get_post.like_count -=1 
                get_post.save()
                results =  {
                    'status':'un-like',
                    'new_count':get_post.like_count,

                }
            else: 
                UserHelpLikes.objects.create(user=request.user,post=get_post)
                get_post.like_count +=1 
                get_post.save()

                n = Notifications.objects.create(title="Yardım Paylaşımını beğendi",sender=request.user.username,link='/yardim/?post_id={}'.format(post_id),system=False)
                NotificationsUsers.objects.create(user=request.user,notification=n)

                results =  {
                    'status':'like',
                    'new_count':get_post.like_count,
                }



            return Response(results,status=status.HTTP_200_OK)
        except:
            return Response({'status':'error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status':'error'},status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
@course_custom_permission('course')
def helpCommentLike(request):

    comment_id = request.GET.get('comment_id',None)
    post_id = request.GET.get('post_id',None)
    if comment_id:

        try:
            get_comment = get_object_or_404(HelpComments,id=comment_id)
            ubl = UserHelpCommentLikes.objects.filter(user=request.user,comment=get_comment).last()

            results =  {
                'status':'no'
            }

            if ubl:
                ubl.delete()
                get_comment.like_count -=1 
                get_comment.save()
                results =  {
                    'status':'un-like',
                    'new_count':get_comment.like_count,

                }
            else: 
                UserHelpCommentLikes.objects.create(user=request.user,comment=get_comment)
                get_comment.like_count +=1 
                get_comment.save()

                n = Notifications.objects.create(title="Yorumunu beğendi",sender=request.user.username,link='/yardim/?post_id={}'.format(post_id),system=False)
                NotificationsUsers.objects.create(user=request.user,notification=n)

                results =  {
                    'status':'like',
                    'new_count':get_comment.like_count,
                }



            return Response(results,status=status.HTTP_200_OK)
        except:
            return Response({'status':'error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status':'error'},status=status.HTTP_403_FORBIDDEN)

