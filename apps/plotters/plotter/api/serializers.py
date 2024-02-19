from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from plotter.models import Car, Files
from plotter.models import Year, Application, Body, Make, Model, Trim, Car, Images, BodyPart

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class BodySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Body)
    class Meta:
        model = Body
        exclude = ("modified",)

class ApplicationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Application)
    class Meta:
        model = Application
        exclude = ("modified",)

class BodyPartSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BodyPart)
    application = ApplicationSerializer()
    class Meta:
        model = BodyPart
        exclude = ("modified",)

class MakeSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Make)

    class Meta:
        model = Make
        exclude = ("modified",)

class ModelSerializer(TranslatableModelSerializer):
    make = MakeSerializer()
    translations = TranslatedFieldsField(shared_model=Model)

    class Meta:
        model = Model
        exclude = ("modified",)

class TrimSerializer(TranslatableModelSerializer):
    model = ModelSerializer()
    translations = TranslatedFieldsField(shared_model=Trim)

    class Meta:
        model = Trim
        exclude = ("modified",)

class CarSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Car)
    trim = TrimSerializer()
    year = YearSerializer(many=True)
    body = BodySerializer()

    class Meta:
        model = Car
        exclude = ("modified",)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)

    #     # Include nested serializers for related models
    #     data['trim'] = TrimSerializer(instance.trim).data
    #     data['year'] = YearSerializer(instance.year).data

    #     # Include any other related models in a similar way
    #     # data['some_related_model'] = SomeRelatedModelSerializer(instance.some_related_model).data

    #     return data


class ImagesSerializer(TranslatableModelSerializer):
    class Meta:
        model = Images
        exclude = ("modified",)


class FilesSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    body_part = BodyPartSerializer()

    class Meta:
        model = Files
        exclude = ("modified",)



# # Include all serializers in a single serializer class
# class AllModelsSerializer:
#     application = ApplicationSerializer()
#     body = BodySerializer()
#     make = MakeSerializer()
#     model = ModelSerializer()
#     trim = TrimSerializer()
#     car = CarSerializer()
#     images = ImagesSerializer()


