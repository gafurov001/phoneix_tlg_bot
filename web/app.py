import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from config import secret_key
from models import Question, Answer, Complaint, engine
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key)
]

app = Starlette(middleware=middleware)

logo_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShnGH75UxzraHXAA39i9M2_cJtioXbcGUigw&s'
admin = Admin(
    engine=engine,
    title="Aiogram Web Admin",
    base_url='/',
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider()
)


# class ProductModelView(ModelView):
#     exclude_fields_from_list = ('created_at', 'updated_at')
#     exclude_fields_from_create = ('created_at', 'updated_at')
#     exclude_fields_from_edit = ('created_at', 'updated_at')
#
#
# class UserModelView(ModelView):
#     exclude_fields_from_edit = ('created_at', 'updated_at')
#
#
# class CategoryModelView(ModelView):
#     exclude_fields_from_create = ('created_at', 'updated_at')
#     exclude_fields_from_edit = ('created_at', 'updated_at')


admin.add_view(ModelView(Complaint))

# Mount admin to your app
admin.mount_to(app)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8088)