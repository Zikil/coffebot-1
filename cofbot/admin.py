from django.contrib import admin
from django.db.models import fields
from telegram import message
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

import telegram

TOKEN = '1033970790:AAHgVbhB3yDw38jC4CIiEoi6jzbP5k_h0HQ'
bot = telegram.Bot(TOKEN)

def send_mes_to_users(text, users):
    for u in users:
        bot.sendMessage(chat_id=u, text=text)


class OrderInLineAdmin(admin.TabularInline):
    model = Order


@admin.register(Buying)
class BuyingAdmin(admin.ModelAdmin):
    inlines = [OrderInLineAdmin]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'name', 'code', 'score', 'messages')
    actions = ['send_mes']

    def messages(self, obj):
        count = obj.message_set.count()
        url = (
            reverse("admin:cofbot_message_changelist")
            + "?"
            + urlencode({"profile": f"{obj.tg_id}"})
        )
        return format_html('<a href="{}">{} Messages</a>', url, count)

    def send_mes(self, request, queryset):
        if 'apply' in request.POST:  
            mes_text = request.POST['text']
            users= []
            for u in queryset:
                users.append(u.tg_id)
            # print(users)
            send_mes_to_users(mes_text, users)
            self.message_user(request, "mes was be send")
            return HttpResponseRedirect(request.get_full_path())
        form = BroadcastForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        # print(request.POST)
        return render(request, "admin/broadcast_message.html", {'items': queryset, 'form': form})


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'profile')

@admin.register(Barista)
class BaristaAdmin(admin.ModelAdmin):
    list_display = ['User', 'full_name1']

    def full_name1(self, obj):
        return f'{obj.User.first_name} {obj.User.last_name}'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('Buying', 'Product', 'Count')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Price')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Ingred', 'Count_ingred')

@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Count')


# @admin.register()
