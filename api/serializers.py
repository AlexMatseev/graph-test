from rest_framework import serializers
from graphs.models import VectorModel, OperatorModel


class OperatorSerializer(serializers.ModelSerializer):
	node_child = serializers.StringRelatedField()

	class Meta:
		model = OperatorModel
		fields = ('id', 'value', 'node_child')


class VectorSerializer(serializers.ModelSerializer):
	operator_child = OperatorSerializer()

	class Meta:
		model = VectorModel
		fields = ('id', 'node_value', 'operator_child')


class CreateUpdateVectorSerializer(serializers.ModelSerializer):

	class Meta:
		model = VectorModel
		fields = ('id', 'node_value')


class CreateUpdateOperatorSerializer(serializers.ModelSerializer):

	class Meta:
		model = OperatorModel
		fields = ('id', 'value')
