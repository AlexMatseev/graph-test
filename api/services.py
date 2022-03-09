import json
from typing import Any

import numpy
import numpy as np
from django.db.models import QuerySet
from numpy.linalg import norm


def get_parents(operator: str, parents: list) -> Any:
	"""
	Binding an operator to parent vectors
	that have null specified in the operator_child field.
	Compares the lengths of vectors and corrects
	by adding a null element to a vector with a shorter value length.

	:param operator: str
	:param parents: list
	:return: Any
	"""
	jsonDec = json.decoder.JSONDecoder()
	parent_list = [jsonDec.decode(i.node_value) for i in parents]
	if len(parent_list) > 1:
		max_len_element = max(parent_list, key=len)
		max_len = len(max_len_element)
		for parent in range(len(parents)):
			current_value = jsonDec.decode(parents[parent].node_value)
			if max_len > len(current_value):
				current_value.append(0)
				node_value = json.dumps(current_value)
				parents[parent].node_value = node_value

		for i in parents:
			i.operator_child = operator
			i.save()

		return parents


def calculate_value(value: str, parents: QuerySet):
	"""
	Calculates the value of the resulting vector
	depending on the values of the parent vectors and the operator.
	:param value: str
	:param parents: Queryset
	:return: Any
	"""
	jsonDec = json.decoder.JSONDecoder()
	if len(parents) > 1:
		result = []
		res_values = jsonDec.decode(parents[0].node_value)
		res_values_int = [int(i) for i in res_values]
		res_values_vector = np.array(res_values_int)
		if value == '+':
			result = get_sum(res_values_vector, parents, jsonDec)
		elif value == '-':
			result = get_sub(res_values_vector, parents, jsonDec)
		elif value == '*':
			result = get_mul(res_values_vector, parents, jsonDec)
		elif value == '/':
			result = get_div(res_values_vector, parents, jsonDec)
		elif value == 'n':
			result = get_length(parents, jsonDec)
		node_value = result.tolist()
		return node_value


def get_sum(
		value_vector_list: numpy.ndarray,
		parents: QuerySet,
		jsonDec: json.decoder.JSONDecoder) -> numpy.ndarray:
	"""
	The operation of adding parent vectors,
	the result of calculating the value for the child vector

	:param value_vector_list: numpy.ndarray
	:param parents:QuerySet
	:param jsonDec: json.decoder.JSONDecoder
	:return: numpy.ndarray
	"""
	print(type(value_vector_list))
	print(type(parents))
	print(type(jsonDec))
	for i in range(1, len(parents)):
		current_value = jsonDec.decode(parents[i].node_value)
		int_value = [int(i) for i in current_value]
		value_array = np.array(int_value)
		result = value_vector_list + value_array
		value_vector_list = result
	return value_vector_list


def get_sub(
		value_vector_list: numpy.ndarray,
		parents: QuerySet,
		jsonDec: json.decoder.JSONDecoder) -> numpy.ndarray:
	"""
	The operation of subtracting parent vectors,
	the result of calculating the value for the child vector

	:param value_vector_list: numpy.ndarray
	:param parents:QuerySet
	:param jsonDec: json.decoder.JSONDecoder
	:return: numpy.ndarray
	"""
	for i in range(1, len(parents)):
		current_value = jsonDec.decode(parents[i].node_value)
		int_value = [int(i) for i in current_value]
		value_array = np.array(int_value)
		result = value_vector_list - value_array
		value_vector_list = result
	return value_vector_list


def get_mul(
		value_vector_list: numpy.ndarray,
		parents: QuerySet,
		jsonDec: json.decoder.JSONDecoder) -> numpy.ndarray:
	"""
	The operation of multiplying parent vectors,
	the result of calculating the value for the child vector

	:param value_vector_list: numpy.ndarray
	:param parents:QuerySet
	:param jsonDec: json.decoder.JSONDecoder
	:return: numpy.ndarray
	"""
	for i in range(1, len(parents)):
		current_value = jsonDec.decode(parents[i].node_value)
		int_value = [int(i) for i in current_value]
		value_array = np.array(int_value)
		result = value_vector_list * value_array
		value_vector_list = result
	return value_vector_list


def get_div(
		value_vector_list: numpy.ndarray,
		parents: QuerySet,
		jsonDec: json.decoder.JSONDecoder) -> numpy.ndarray:
	"""
	The operation of dividing parent vectors,
	the result of calculating the value for the child vector

	:param value_vector_list: numpy.ndarray
	:param parents:QuerySet
	:param jsonDec: json.decoder.JSONDecoder
	:return: numpy.ndarray
	"""
	for i in range(1, len(parents)):
		current_value = jsonDec.decode(parents[i].node_value)
		int_value = [int(i) for i in current_value]
		value_array = np.array(int_value)
		result = value_vector_list / value_array
		value_vector_list = result
	return value_vector_list


def get_length(
		parents: QuerySet,
		jsonDec: json.decoder.JSONDecoder) -> numpy.ndarray:
	"""
	The length of the vector is calculated
	:param parents: QuerySet
	:param jsonDec: json.decoder.JsonDecoder
	:return: numpy.ndarray
	"""
	res_list = []
	for i in range(len(parents)):
		current_value = jsonDec.decode(parents[i].node_value)
		int_value = [int(i) for i in current_value]
		value_array = np.array(int_value)
		norm_arr = norm(value_array)
		res_list.append(round(norm_arr, 2))
	value_vector_list = np.array(res_list)
	return value_vector_list
