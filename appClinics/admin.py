from appClinics import db, app, dao
from appClinics.models import UserRole, Regulations, Medicine
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')

        return super().__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MedicineView(AuthenticatedModelView):
    column_searchable_list = ['name', 'content']
    column_filters = ['name', 'price']
    can_view_details = True
    column_exclude_list = ['description']
    can_export = True
    column_export_list = ['id', 'name', 'content', 'price']
    column_labels = {
        'name': 'Tên thuốc',
        'content': 'Mô tả',
        'price': 'Gía'
    }
    page_size = 5
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'content': CKTextAreaField
    }


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app, name='Quản trị bệnh viện', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AuthenticatedModelView(Regulations, db.session, name='Quy định'))
admin.add_view(MedicineView(Medicine, db.session, name='Thuốc'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))