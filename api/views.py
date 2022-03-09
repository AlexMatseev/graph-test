import json

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from api.serializers import VectorSerializer, \
	CreateUpdateOperatorSerializer, CreateUpdateVectorSerializer
from api.services import get_parents
from graphs.models import VectorModel, OperatorModel


class VectorListAPIView(ListAPIView):
	"""
	Returns a list of all vectors, with values and associated operators.
	Reflects the structure of the graph.
	"""
	queryset = VectorModel.objects.all()
	serializer_class = VectorSerializer


class CreateVectorAPIView(CreateAPIView):
	"""
	Creating a new vector with a value of type digit,digit,digit.
	Serializes the value and adds Vector Models to the model as an array.
	When the vector value is received,
	the value is deserialized and converted into
	a numpy array for further work.
	"""
	queryset = VectorModel.objects.all()
	serializer_class = CreateUpdateVectorSerializer

	def perform_create(self, serializer):
		node_value = self.get_value()
		serializer.save(node_value=node_value)

	def get_value(self):
		value = self.request.data.get('node_value', None)
		value_list = value.split(',')
		value = [int(i) for i in value_list]
		node_value = json.dumps(value)
		return node_value


class CreateOperatorAPIView(CreateAPIView):
	"""
	Creating an operator for working with vectors.
	After creating the operator, it binds to the free vectors,
	and creates the resulting vector.
	"""
	queryset = OperatorModel
	serializer_class = CreateUpdateOperatorSerializer

	def perform_create(self, serializer):
		new_operator = serializer.save()
		value = new_operator.value
		parents_query = VectorModel.objects.filter(operator_child=None)
		parents = get_parents(new_operator, parents_query)


class UpdateVectorAPIView(UpdateAPIView):
	"""
	Updating the value of an existing vector.
	When updating the value and saving the object, by receiving a signal,
	the associated resulting vectors are transformed, if it exists.
	"""
	queryset = VectorModel.objects.all()
	serializer_class = CreateUpdateVectorSerializer

	def perform_update(self, serializer):
		node_value = self.get_value()
		serializer.save(node_value=node_value)

	def get_value(self):
		value = self.request.data.get('node_value', None)
		value_list = value.split(',')
		value = [int(i) for i in value_list]
		node_value = json.dumps(value)
		return node_value


class UpdateOperatorAPIView(UpdateAPIView):
	"""
	Updating the value of an existing operator.
	The resulting vector and all associated vectors
	are transformed by the signal.
	"""
	queryset = OperatorModel.objects.all()
	serializer_class = CreateUpdateOperatorSerializer

	def perform_update(self, serializer):
		new_operator = serializer.save()
		value = new_operator.value
		parents_query = VectorModel.objects.filter(operator_child=new_operator)
		parents = get_parents(new_operator, parents_query)


class DeleteVectorAPIView(DestroyAPIView):
	"""
	Deleting the current vector and its associated graph elements.
	"""
	queryset = VectorModel.objects.all()
	serializer_class = CreateUpdateVectorSerializer


class DeleteOperatorAPIView(DestroyAPIView):
	"""
	Deleting the current operator, and related graph elements.
	"""
	queryset = OperatorModel.objects.all()
	serializer_class = CreateUpdateOperatorSerializer
