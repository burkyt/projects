from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf.urls.static import static
from conf.views import main_page, product, cart, add_to_cart, task_process, task_done, product_detail, auth, sign_out, \
    sign_up
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("__debug__/", include("debug_toolbar.urls")),
                  path("", main_page, name="main_page"),
                  path("login/", auth, name="login"),
                  path("logout/", sign_out, name="logout"),
                  path("register/", sign_up, name="register"),
                  path("add/cart/<int:id>/", add_to_cart, name="add_cart"),
                  path("cart/", cart, name="cart_page"),
                  path("category/<int:id>/", product, name="product"),
                  path('tasks/', task_process, name="tasks"),
                  path('tasks/<int:id>/done/', task_done, name='done'),
                  path('product/<int:product_id>/', product_detail, name='product-detail')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
