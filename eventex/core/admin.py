from django.contrib import admin
from django.utils.html import format_html

from eventex.core.models import Speaker


class SpeakerModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['photo_img', 'name', 'website_link']

    def website_link(self, obj):
        website = obj.website
        return format_html(f'<a href="{website}">{website}</a>')

    website_link.short_description = 'website'

    def photo_img(self, obj):
        photo = obj.photo
        return format_html(f'<img width="32px" src="{photo}">')

    photo_img.short_description = 'foto'


admin.site.register(Speaker, SpeakerModelAdmin)
