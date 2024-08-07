
import logging
from flask import Flask, render_template
from flask_appbuilder import AppBuilder, expose, BaseView
from .models import db, App_type, Application, Customers, Device_app_dns, Device_type, Devices, Dns_a_register, Ip_address, Network_interface, Operationalsystem_type, Organization, Provider, Services, Test, Test_app_server, Test_execution_control, Test_result, Test_status, Test_title, Test_topic

# Configuração do logging
logger = logging.getLogger(__name__)

def register_views(app: Flask):
    try:
        appbuilder = AppBuilder(app, db.session)

        
        class App_typeView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(App_type).all()
                return render_template('app_type_list.html', items=items)

        appbuilder.add_view(App_typeView, "App_type", icon="fa-folder-open-o", category="Admin")
        
        class ApplicationView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Application).all()
                return render_template('application_list.html', items=items)

        appbuilder.add_view(ApplicationView, "Application", icon="fa-folder-open-o", category="Admin")
        
        class CustomersView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Customers).all()
                return render_template('customers_list.html', items=items)

        appbuilder.add_view(CustomersView, "Customers", icon="fa-folder-open-o", category="Admin")
        
        class Device_app_dnsView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Device_app_dns).all()
                return render_template('device_app_dns_list.html', items=items)

        appbuilder.add_view(Device_app_dnsView, "Device_app_dns", icon="fa-folder-open-o", category="Admin")
        
        class Device_typeView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Device_type).all()
                return render_template('device_type_list.html', items=items)

        appbuilder.add_view(Device_typeView, "Device_type", icon="fa-folder-open-o", category="Admin")
        
        class DevicesView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Devices).all()
                return render_template('devices_list.html', items=items)

        appbuilder.add_view(DevicesView, "Devices", icon="fa-folder-open-o", category="Admin")
        
        class Dns_a_registerView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Dns_a_register).all()
                return render_template('dns_a_register_list.html', items=items)

        appbuilder.add_view(Dns_a_registerView, "Dns_a_register", icon="fa-folder-open-o", category="Admin")
        
        class Ip_addressView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Ip_address).all()
                return render_template('ip_address_list.html', items=items)

        appbuilder.add_view(Ip_addressView, "Ip_address", icon="fa-folder-open-o", category="Admin")
        
        class Network_interfaceView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Network_interface).all()
                return render_template('network_interface_list.html', items=items)

        appbuilder.add_view(Network_interfaceView, "Network_interface", icon="fa-folder-open-o", category="Admin")
        
        class Operationalsystem_typeView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Operationalsystem_type).all()
                return render_template('operationalsystem_type_list.html', items=items)

        appbuilder.add_view(Operationalsystem_typeView, "Operationalsystem_type", icon="fa-folder-open-o", category="Admin")
        
        class OrganizationView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Organization).all()
                return render_template('organization_list.html', items=items)

        appbuilder.add_view(OrganizationView, "Organization", icon="fa-folder-open-o", category="Admin")
        
        class ProviderView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Provider).all()
                return render_template('provider_list.html', items=items)

        appbuilder.add_view(ProviderView, "Provider", icon="fa-folder-open-o", category="Admin")
        
        class ServicesView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Services).all()
                return render_template('services_list.html', items=items)

        appbuilder.add_view(ServicesView, "Services", icon="fa-folder-open-o", category="Admin")
        
        class TestView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test).all()
                return render_template('test_list.html', items=items)

        appbuilder.add_view(TestView, "Test", icon="fa-folder-open-o", category="Admin")
        
        class Test_app_serverView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test_app_server).all()
                return render_template('test_app_server_list.html', items=items)

        appbuilder.add_view(Test_app_serverView, "Test_app_server", icon="fa-folder-open-o", category="Admin")
        
        class Test_execution_controlView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test_execution_control).all()
                return render_template('test_execution_control_list.html', items=items)

        appbuilder.add_view(Test_execution_controlView, "Test_execution_control", icon="fa-folder-open-o", category="Admin")
        
        class Test_resultView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test_result).all()
                return render_template('test_result_list.html', items=items)

        appbuilder.add_view(Test_resultView, "Test_result", icon="fa-folder-open-o", category="Admin")
        
        class Test_statusView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test_status).all()
                return render_template('test_status_list.html', items=items)

        appbuilder.add_view(Test_statusView, "Test_status", icon="fa-folder-open-o", category="Admin")
        
        class Test_titleView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test_title).all()
                return render_template('test_title_list.html', items=items)

        appbuilder.add_view(Test_titleView, "Test_title", icon="fa-folder-open-o", category="Admin")
        
        class Test_topicView(BaseView):
            default_view = 'list'

            @expose('/list/')
            def list(self):
                items = db.session.query(Test_topic).all()
                return render_template('test_topic_list.html', items=items)

        appbuilder.add_view(Test_topicView, "Test_topic", icon="fa-folder-open-o", category="Admin")
        

        logger.info("Views registradas com sucesso.")

    except Exception as e:
        logger.error("Erro ao registrar as views: %s", e)
        raise