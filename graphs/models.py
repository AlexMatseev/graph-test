from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.services import calculate_value


class VectorModel(models.Model):
    node_value = models.CharField(max_length=255, null=True, blank=True)
    operator_child = models.ForeignKey(
        "OperatorModel",
        on_delete=models.CASCADE,
        related_name='vector_parent',
        blank=True,
        null=True)

    def __str__(self):
        return f'{self.node_value}'


@receiver(post_save, sender=VectorModel)
def update_node_values(instance, **kwargs):
    try:
        current_operator = OperatorModel.objects.get(vector_parent__pk=instance.id)
    except OperatorModel.DoesNotExist:
        current_operator = None
    if current_operator:
        update_operator_values(current_operator, **kwargs)


class OperatorModel(models.Model):
    OPERATOR_CHOICES = (
        ('+', 'sum'),
        ('-', 'sub'),
        ('*', 'mul'),
        ('/', 'div'),
        ('n', 'length')
    )
    value = models.CharField(
        choices=OPERATOR_CHOICES, max_length=1, default='+')
    node_child = models.OneToOneField(
        VectorModel,
        on_delete=models.CASCADE,
        related_name='operator_parent', null=True, blank=True)

    def __str__(self):
        return f'{self.value}'


@receiver(post_save, sender=OperatorModel)
def update_operator_values(instance, **kwargs):

    parents = VectorModel.objects.filter(operator_child__pk=instance.id)
    if len(parents) > 1:
        child_value = calculate_value(instance.value, parents)
        if not instance.node_child:
            child_vector = VectorModel.objects.create(node_value=child_value)
            instance.node_child = child_vector
            instance.save()
        else:
            update_child = VectorModel.objects.get(operator_parent=instance)
            update_child.node_value = child_value
            update_child.save()
