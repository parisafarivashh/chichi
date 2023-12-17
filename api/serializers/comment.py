from rest_framework.serializers import ModelSerializer

from ..models import Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'body', 'is_approved', 'created_by', 'product']

        extra_kwargs = {
            'is_approved': {'required': False},
            'created_by': {'required': False},
            'product': {'required': False},
        }

        def create(self, validated_data):
            # Make the field not required for updates
            self.fields['body'].required = True
            return super(validated_data).create()

        def update(self, instance, validated_data):
            # Make the field not required for updates
            self.fields['body'].required = False
            return super(instance, validated_data).update()

