from django.http import Http404
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import *  
from homepage.models import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class CombinedSiteDataView(APIView):
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        try:
            site_information = SiteInformation.objects.first()
            site_metadata = SiteMetaData.objects.first()
            site_information_additional = SiteInformationAdditional.objects.first()

            if site_information and site_metadata and site_information_additional:
                # Serialize data from each model
                site_information_data = SiteInformationSerializer(site_information).data
                site_metadata_data = SiteMetaDataSerializer(site_metadata).data
                site_information_additional_data = SiteInformationAdditionalSerializer(site_information_additional).data

                # Combine data from all models into a single response
                combined_data = {
                    'site_information': site_information_data,
                    'site_metadata': site_metadata_data,
                    'site_information_additional': site_information_additional_data,
                }

                return Response(combined_data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class NoPagination(PageNumberPagination):
    page_size = None

class SiteInformationListView(APIView):
    serializer_class = SiteInformationSerializer
    
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            site_information_objects = SiteInformation.objects.all()
            if site_information_objects:
                serializer = self.serializer_class(site_information_objects, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SiteInformationView(APIView):
    serializer_class = SiteInformationSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            first_object = SiteInformation.objects.first()
            if first_object:
                serializer = self.serializer_class(first_object)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SiteMetaDataListView(APIView):
    serializer_class = SiteMetaDataSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            site_metadata_objects = SiteMetaData.objects.all()
            if site_metadata_objects:
                serializer = self.serializer_class(site_metadata_objects, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteMetaData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SiteInformationAdditionalListView(APIView):
    serializer_class = SiteInformationAdditionalSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            site_information_additional_objects = SiteInformationAdditional.objects.all()
            if site_information_additional_objects:
                serializer = self.serializer_class(site_information_additional_objects, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteInformationAdditional.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

# class SiteInformationListView(generics.ListAPIView):
#     serializer_class = SiteInformationSerializer
    
#     def get_queryset(self):
#         return SiteInformation.objects.all()

# class SiteMetaDataListView(generics.ListAPIView):
#     serializer_class = SiteMetaDataSerializer

#     def get_queryset(self):
#         return SiteMetaData.objects.all()

# class SiteInformationAdditionalListView(generics.ListAPIView):
#     serializer_class = SiteInformationAdditionalSerializer

#     def get_queryset(self):
#         return SiteInformationAdditional.objects.all()

class CustomModelDataView(generics.ListAPIView):
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    serializer_class_mapping = {
        'marketing': MarketingSerializer,
        'service': ServiceSerializer,
        'feature': FeatureSerializer,
        'offering': OfferingSerializer,
        'project': ProjectSerializer,
        'teammember': TeammemberSerializer,
        'testimonial': TestimonialSerializer,
    }
    def get_serializer_class(self):
        model_name = self.kwargs.get('model_name')
        return self.serializer_class_mapping.get(model_name, None)

    
    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        if model_name in self.serializer_class_mapping:
            model_class = self.serializer_class_mapping[model_name].Meta.model
            return model_class.objects.all()
        return None




# @csrf_exempt
# def site_information(request):
#     # Get the first object as a JSON array
#     if request.method == 'GET':
#         site_information = SiteInformation.objects.first()
#         if site_information:
#             site_information_serializer = SiteInformationSerializer([site_information], many=True)
#             return JsonResponse(site_information_serializer.data, safe=False)
#         else:
#             return JsonResponse([], safe=False)

# @csrf_exempt
# @api_view(['GET'])
# def site_information(request):
#     if request.method == 'GET':
#         site_information = SiteInformation.objects.first()
#         if site_information:
#             site_information_serializer = SiteInformationSerializer(site_information)
#             site_metadata = SiteMetaData.objects.first()
#             site_metadata_serializer = SiteMetaDataSerializer(site_metadata) if site_metadata else None
#             site_info_additional = SiteInformationAdditional.objects.first()
#             site_info_additional_serializer = SiteInformationAdditionalSerializer(site_info_additional) if site_info_additional else None

#             response_data = {
#                 'site_information': site_information_serializer.data,
#                 'site_metadata': site_metadata_serializer.data if site_metadata_serializer else None,
#                 'site_information_additional': site_info_additional_serializer.data if site_info_additional_serializer else None
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)






# @api_view(['GET'])
# def get_data_for_model(request, model_name):
    
#     model_mapping = {
#         'marketing': Marketing,
#         'service': Service,
#         'feature': Feature,
#         # 'category': Category,
#         # 'post': Post,
#         # 'productcategory': ProductCategory,
#         'offering': Offering,
#         'project': Project,
#         'teammember': TeamMember,
#         'testimonial': Testimonial,
#     }

#     if model_name in model_mapping:
#         model_class = model_mapping[model_name]
#         objects = model_class.objects.all()
#         serializer_class = globals()[f'{model_name.capitalize()}Serializer']
#         serializer = serializer_class(objects, many=True)
#         return Response(serializer.data)

#     return Response({'error': 'Invalid model name'}, status=status.HTTP_400_BAD_REQUEST)





# @api_view(['GET'])
# @csrf_exempt
# def site_information_json(request):
#     try:
#         site_info = SiteInformation.objects.first()
#         if site_info:
#             serializer = SiteInformationSerializer(site_info)
#             print(serializer.data)
#             return JsonResponse(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({"error": "No site information found"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @csrf_exempt
# def site_information_json(request):
#     #Get all
#     if request.method == 'GET':
#         schedules = SiteInformation.objects.all()
#         schedules_serializer = SiteInformationSerializer(schedules,many=True)
#         print(schedules_serializer.data)
#         return JsonResponse(schedules_serializer.data, safe=False)

# class SiteInformationAPIView(views.APIView):
#     serializer_class = SiteInformationSerializer
#     renderer_classes = (Renderer,)
#     permission_classes = (permissions.AllowAny, )

#     def get(self, request):
        
#         info = SiteInformation.objects.all()
#         if len(info) != 1:
#             raise Http404('Information for this site is not posted.')
        
#         info = info[0]

#         serializer = self.serializer_class(info)

#         return Response(serializer.data, status=status.HTTP_200_OK)


def index(request):
    import os
    # List of JavaScript filenames
    # Path to your static folder
    static_folder = os.path.join(settings.BASE_DIR, "static")

    # List of JavaScript filenames from the static folder
    js_files = [f for f in os.listdir(static_folder) if f.endswith('.js')]
    # print(js_files)
    context = {
        "js_files": js_files,
    }
    return render(request, 'index.html', context)


def home(request):
    # info = SiteInformation.objects.all()
    # if len(info) != 1:
    #     raise Http404('Information for this site is not posted.')
    # info = info[0]
    
    services = Service.objects.all()
    projects = Project.objects.filter(is_published=True).order_by('-updated_at')
    features = Feature.objects.all()
    offerings = Offering.objects.all()
    marketings = Marketing.objects.all()
    teammembers = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        # 'site_information': info,
        'services': services,
        'projects': projects,
        'features': features,
        'offerings': offerings,
        'marketings': marketings,
        'teammembers': teammembers,
        'testimonials': testimonials,
        'copyright': f'2000-{dt.now().year}',	
    }
    return render(request, 'index.html', context)





# from django.views.generic import ListView
# from django.views.generic import DetailView
# from .models import Category, Post


# def blog(request):
#     categories = Category.objects.all()
#     posts = Post.objects.all()

#     context = {
#         'categories': categories,
#         'posts': posts,
#     }
#     return render(request, 'blog/blogs.html', context)



# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'  # Create this template
#     context_object_name = 'posts'
#     ordering = ['-created_at']
#     paginate_by = 10  # Adjust as needed


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'  # Create this template
#     context_object_name = 'post'


# class CategoryListView(ListView):
#     model = Category
#     template_name = 'blog/category_list.html'  # Create this template
#     context_object_name = 'categories'


# class CategoryDetailView(ListView):
#     template_name = 'blog/category_detail.html'  # Create this template
#     context_object_name = 'category_posts'
#     paginate_by = 10  # Adjust as needed

#     def get_queryset(self):
#         category = Category.objects.get(slug=self.kwargs['slug'])
#         return Post.objects.filter(categories=category).order_by('-created_at')


# def bootstrap(request):
# 	context = {
# 	}
# 	return render(request, 'bootstrap.html', context)