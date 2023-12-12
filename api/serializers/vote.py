from rest_framework.serializers import ModelSerializer

from ..models import Vote


class VoteSerializer(ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id', 'rate', 'created_by', 'product']
        extra_kwargs = {
            'created_by': {
                'required': False,
            },
            'product': {
                'required': False,
            }
        }

