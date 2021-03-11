from abc import ABC

from rest_framework import serializers

from movies.models import Movie, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Comments filter, only for parent"""
    # data = queryset
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super(FilterReviewListSerializer, self).to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        # serializer = self.parent.parent.__class__(instance, context=self.context)
        serializer = ReviewSerializer(instance, context=self.context)
        return serializer.data


class MovieSerializer(serializers.ModelSerializer):
    """Films list"""

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class CreateReviewsSerializer(serializers.ModelSerializer):
    """ Add review """

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """List all reviews"""
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Review
        list_serializer_class = FilterReviewListSerializer
        fields = ("name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Film details """

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    actors = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateReviewsSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model=Movie
        exclude = ("star", "movie")


    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )

        return rating