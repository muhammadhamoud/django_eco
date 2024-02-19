from rest_framework import serializers

from homepage.models import (
    SiteInformation, Marketing, Service, Feature, 
    BusinessCategory, Offering, Project, TeamMember, 
    Testimonial, SiteMetaData, SiteInformationAdditional
    )

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

class SiteInformationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteInformation)
    class Meta:
        model = SiteInformation
        fields = '__all__'

class SiteMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteMetaData
        exclude = ("modified",)

class SiteInformationAdditionalSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteInformationAdditional)
    class Meta:
        model = SiteInformationAdditional
        fields = '__all__'

class MarketingSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Marketing)

    class Meta:
        model = Marketing
        fields = '__all__'

class ServiceSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Service)
    class Meta:
        model = Service
        fields = '__all__'

class FeatureSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Feature)
    class Meta:
        model = Feature
        fields = '__all__'

class BusinessCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BusinessCategory)
    class Meta:
        model = BusinessCategory
        fields = '__all__'

class OfferingSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Offering)
    class Meta:
        model = Offering
        fields = '__all__'

class ProjectSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Project)
    category = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_category(self, obj):
        return obj.category.name

class TeammemberSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TeamMember)
    class Meta:
        model = TeamMember
        fields = '__all__'

class TestimonialSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Testimonial)
    class Meta:
        model = Testimonial
        fields = '__all__'


# class IndexDataSerializer(serializers.Serializer):
#     services = serializers.SerializerMethodField()
#     projects = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()
#     offerings = serializers.SerializerMethodField()
#     marketings = serializers.SerializerMethodField()
#     teammembers = serializers.SerializerMethodField()
#     testimonials = serializers.SerializerMethodField()
#     copyright = serializers.CharField()

#     def get_services(self, obj):
#         services = Service.objects.all()
#         # You can serialize the services data here if needed
#         return services

#     def get_projects(self, obj):
#         projects = Project.objects.filter(is_published=True).order_by('-updated_at')
#         # You can serialize the projects data here if needed
#         return projects

#     def get_features(self, obj):
#         features = Feature.objects.all()
#         # You can serialize the features data here if needed
#         return features

#     def get_offerings(self, obj):
#         offerings = Offering.objects.all()
#         # You can serialize the products data here if needed
#         return offerings

#     def get_marketings(self, obj):
#         marketings = Marketing.objects.all()
#         # You can serialize the marketings data here if needed
#         return marketings

#     def get_teammembers(self, obj):
#         teammembers = TeamMember.objects.all()
#         # You can serialize the teammembers data here if needed
#         return teammembers

#     def get_testimonials(self, obj):
#         testimonials = Testimonial.objects.all()
#         # You can serialize the testimonials data here if needed
#         return testimonials