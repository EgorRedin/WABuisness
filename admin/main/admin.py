from django.contrib import admin
from .models import User, UserMaterials, Material, Question, Keyword
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.timezone import make_aware
from datetime import UTC
class KeywordResource(resources.ModelResource):
    class Meta:
        model = Keyword


class UserResource(resources.ModelResource):
    class Meta:
        model = User

    def dehydrate_date(self, user):
        if user.date:
            return make_aware(user.date, timezone=UTC)
        return None


class UserAdminInline(admin.TabularInline):
    model = User


class KeywordAdmin(ImportExportModelAdmin):
    list_display = ["id", "key_word"]
    list_editable = ["key_word"]
    inlines = [UserAdminInline]
    resource_classes = [KeywordResource]


class UserMaterialsResource(resources.ModelResource):
    class Meta:
        model = UserMaterials
        exclude = ("user", "material")

    def dehydrate_date(self, user_material):
        if user_material.date:
            return make_aware(user_material.date, timezone=UTC)
        return None


class UserMaterialsAdmin(ImportExportModelAdmin):

    model = Material.users.through

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ["user_phone", "count", "material_name", "date"]
    resource_classes = [UserMaterialsResource]


class UserMaterialsInLine(admin.TabularInline):
    model = UserMaterials


class UserAdmin(ImportExportModelAdmin):
    list_display = ["id", "phone_number", "name", "role", "chat_id", "date", "region"]
    list_editable = ["phone_number", "name", "role", "chat_id", "date", "region"]
    inlines = [UserMaterialsInLine]
    resource_classes = [UserResource]


class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material


class MaterialAdmin(ImportExportModelAdmin):
    list_display = ["id", "name", "key_word"]
    list_editable = ["name", "key_word"]
    inlines = [UserMaterialsInLine]
    resource_classes = [MaterialResource]


class MaterialAdminInline(admin.ModelAdmin):
    model = Material


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ["id", "phone_number", "question"]
    list_editable = ["phone_number", "question"]


admin.site.register(User, UserAdmin)
admin.site.register(UserMaterials, UserMaterialsAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Keyword, KeywordAdmin)


