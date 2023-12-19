from rest_framework.serializers import ModelSerializer

from ..models import Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'body', 'is_approved', 'created_by', 'product']
        read_only_fields = ['created_by', 'product']

        def create(self, validated_data):
            # Make the field not required for updates
            self.fields['body'].required = True
            return super(validated_data).create()

        def update(self, instance, validated_data):
            # Make the field not required for updates
            self.fields['body'].required = False
            return super(instance, validated_data).update()

