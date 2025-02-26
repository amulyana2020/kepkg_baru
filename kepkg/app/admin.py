from django.contrib import admin
from .models import Profile, Status, Reviewer, Review, Decision, Resubmission, News

admin.site.register(Reviewer)
admin.site.register(Decision)
admin.site.register(Resubmission)


# Register your models here.
@admin.register(Profile)
class ProfiledAdmin(admin.ModelAdmin):
    list_display = ["fullname", "gender", "mobile"]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["submission", "status", 'category']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["submission", "file_review"]

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at"]