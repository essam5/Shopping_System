import json
import serpy
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductViews

# from drf_haystack.serializers import HaystackSerializer
# from .search_indexes import ProductIndex


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["updated"]


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = ["updated"]


class SerpyProductSerializer(serpy.Serializer):
    seller = serpy.StrField()
    category = serpy.StrField()
    title = serpy.StrField()
    price = serpy.FloatField()
    image = serpy.StrField()
    description = serpy.StrField()
    quantity = serpy.IntField()
    views = serpy.IntField()


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["updated"]
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = ["updated"]


class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        exclude = ["updated"]


# class ProductIndexSerializer(HaystackSerializer):
#     class Meta:
#         # The `index_classes` attribute is a list of which search indexes
#         # we want to include in the search.
#         index_classes = [ProductIndex]

#         # The `fields` contains all the fields we want to include.
#         # NOTE: Make sure you don't confuse these with model attributes. These
#         # fields belong to the search index!
#         fields = (
#             "text",
#             "title",
#             "category",
#         )
