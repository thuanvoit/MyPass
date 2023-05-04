from os import name
from django.urls import path
from . import views
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("password", views.password, name="password_view"),
    path("note", views.note, name="note_view"),
    path("address", views.address, name="address_view"),
    path("card", views.card, name="card_view"),
    path("bankaccount", views.bankaccount, name="bankaccount_view"),
    path("profile", views.profile, name="profile"),


    #APIs
    path("star/<str:pageCode>/<uuid:id>", views.star_item, name="star_item"),

    path("getpassword/<uuid:id>", views.get_password, name="get_password"),
    path("getcard/<uuid:id>", views.get_card, name="get_card"),
    path("getbankaccount/<uuid:id>", views.get_bankaccount, name="get_bankaccount"),


    path("delete_item/<str:pageCode>/<uuid:pass_id>", views.delete_item, name="delete_item"),
    path("getit/<str:pageCode>/<uuid:id>", views.get_it, name="get_it"),
    path("saveEditItem/<str:pageCode>/<uuid:id>", views.save_edit_item, name="save_edit_item"),
    path("copyit", views.copyit, name="copyit"),
    path("changePassword", views.change_password, name="change_password"),
    path("deleteAccount", views.delete_account, name="delete_account"),
    path("checkCard", views.check_card, name="check_card"),
    path("editAccountInfo", views.edit_account_info, name="edit_account_info"),


    #SHARE
    path("share-note/<str:share_url>", views.share_note, name="share_note"),
    path("share-address/<str:share_url>", views.share_address, name="share_address"),

]