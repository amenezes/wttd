from django.contrib import admin
from django.utils.html import format_html

from eventex.core.models import Speaker, Contact, Talk


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['photo_img', 'name', 'website_link', 'email', 'phone']

    def website_link(self, obj):
        website = obj.website
        return format_html(f'<a href="{website}">{website}</a>')

    website_link.short_description = 'website'

    def photo_img(self, obj):
        photo = obj.photo
        return format_html(f'<img width="32px" src="{photo}">')

    photo_img.short_description = 'foto'

    def email(self, obj):
        return obj.contact_set.emails().first()

    email.short_description = 'email'

    def phone(self, obj):
        return obj.contact_set.phones().first()

    photo_img.short_description = 'telefone'


admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)
