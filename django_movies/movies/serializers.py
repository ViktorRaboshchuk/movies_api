from abc import ABC

from rest_framework import serializers

from movies.models import Movie, Review, Rating, Actor


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


class ActorListSerializer(serializers.ModelSerializer):
    """list Actors and Directors"""

    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    """details about Actors and Directors"""

    class Meta:
        model = Actor
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    """Films list"""

    rating_user = serializers.BooleanField()
    middle_star = serializers.DecimalField(max_digits = 10, decimal_places=2)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user', 'middle_star')


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
        fields = ("id", "name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Film details """

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateRatingStarSerializer(serializers.ModelSerializer):
    """Add review"""

    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )

        return rating

