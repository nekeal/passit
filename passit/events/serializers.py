from typing import Dict, Tuple, Any

from django.utils.translation import ugettext as _
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from .models import Event
from ..common.serializers import OwnedModelSerializerMixin
from ..subject.models import SubjectOfAgeGroup
from ..subject.serializers import FieldOfStudyOfAgeGroupSerializer, SubjectOfAgeGroupSerializer


class EventSerializer(OwnedModelSerializerMixin, FlexFieldsModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'category', 'due_date', 'field_age_group', 'subject_group',
                  'created_by', 'modified_by', 'created_by_profile', 'modified_by_profile')
        expandable_fields: Dict[str, Tuple[Serializer, Dict[str, Any]]] = {
            'field_age_group': (FieldOfStudyOfAgeGroupSerializer, {}),
            'subject_group': (SubjectOfAgeGroupSerializer, {"omit": 'subject.field_of_study'}),
        }

    def validate_subject_group(self, value: SubjectOfAgeGroup):
        if value:
            data = self.get_initial()
            if not str(value.field_age_group_id) == str(data['field_age_group']):
                raise ValidationError(_('Subject does not match to field of study'))
        return value
