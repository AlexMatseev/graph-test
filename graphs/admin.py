from django.contrib import admin

from graphs.models import VectorModel, OperatorModel


@admin.register(VectorModel)
class GraphModelAdmin(admin.ModelAdmin):
	pass


@admin.register(OperatorModel)
class GraphModelAdmin(admin.ModelAdmin):
	pass

