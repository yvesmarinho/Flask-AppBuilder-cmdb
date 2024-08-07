import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, PrimaryKeyConstraint, UniqueConstraint, Index, Float
from sqlalchemy.types import JSON, DateTime
from sqlalchemy.orm import relationship


# Models for database: cmdb

class App_type(Model):
    __tablename__ = 'app_type'
    __bind_key__ = 'cmdb'

    id_app_type = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    description = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.description


class Application(Model):
    __tablename__ = 'application'
    __bind_key__ = 'cmdb'

    id_application = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(String(50), default=None)
    id_app_type = Column(Integer, nullable=False, ForeignKey('cmdb.app_type.id_app_type'))
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_app_type = Column(ASC, ForeignKey('cmdb.app_type.id_app_type'))

    def __repr__(self):
        return self.name


class Customers(Model):
    __tablename__ = 'customers'
    __bind_key__ = 'cmdb'

    id_customers = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    customers_name = Column(String(100), nullable=False)
    id_organization = Column(Integer, nullable=False, ForeignKey('cmdb.organization.id_organization'))
    id_site = Column(Integer, nullable=False, ForeignKey('location.sites.id_sites'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None)
    customers_name = Column(ASC)
    id_site = Column(ASC, ForeignKey('location.sites.id_sites'))
    id_organization = Column(ASC, ForeignKey('cmdb.organization.id_organization'))
    UniqueConstraint('', 'customers_name` ASC'),

    def __repr__(self):
        return self.customers_name


class Device_app_dns(Model):
    __tablename__ = 'device_app_dns'
    __bind_key__ = 'cmdb'

    id_device = Column(Integer, nullable=False, ForeignKey('cmdb.devices.id_devices'))
    id_dns = Column(Integer, nullable=False, ForeignKey('cmdb.dns_a_register.id_dns_a_register'))
    id_application = Column(Integer, nullable=False, ForeignKey('cmdb.application.id_application'))
    app_port = Column(Integer, nullable=False)
    server_ip_type = Column(ENUM)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_dns = Column(ASC, ForeignKey('cmdb.dns_a_register.id_dns_a_register'))
    id_device = Column(ASC, ForeignKey('cmdb.devices.id_devices'))
    id_application = Column(ASC, ForeignKey('cmdb.application.id_application'))

    def __repr__(self):
        return self.id_dns


class Device_type(Model):
    __tablename__ = 'device_type'
    __bind_key__ = 'cmdb'

    id_device_type = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    description = Column(String(255), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.description


class Devices(Model):
    __tablename__ = 'devices'
    __bind_key__ = 'cmdb'

    id_devices = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    id_device_type = Column(Integer, nullable=False, ForeignKey('cmdb.device_type.id_device_type'))
    device_name = Column(String(255), nullable=False)
    id_operational_system = Column(Integer, nullable=False, ForeignKey('cmdb.operationalsystem_type.id_operationalsystem_type'))
    id_provider = Column(Integer, nullable=False, ForeignKey('cmdb.provider.id_provider'))
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_device_type = Column(ASC, ForeignKey('cmdb.device_type.id_device_type'))
    id_operational_system = Column(ASC, ForeignKey('cmdb.operationalsystem_type.id_operationalsystem_type'))
    id_provider = Column(ASC, ForeignKey('cmdb.provider.id_provider'))

    def __repr__(self):
        return self.id_device_type


class Dns_a_register(Model):
    __tablename__ = 'dns_a_register'
    __bind_key__ = 'cmdb'

    id_dns_a_register = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    name = Column(String(256), nullable=False)
    comment = Column(Text, default=None)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.name


class Ip_address(Model):
    __tablename__ = 'ip_address'
    __bind_key__ = 'cmdb'

    id_ip_address = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    id_network_interface = Column(Integer, nullable=False, ForeignKey('cmdb.network_interface.id_network_interface'))
    ip_address_name = Column(String(255), nullable=False)
    ip_address_type = Column(ENUM)
    ip_address_version = Column(ENUM)
    ip_address = Column(String(50), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_network_interface = Column(ASC, ForeignKey('cmdb.network_interface.id_network_interface'))
    ip_address_type = Column(ASC)
    ip_address_version = Column(ASC)
    ip_address = Column(ASC)
    UniqueConstraint('', 'id_network_interface` ASC', 'ip_address_type` ASC', 'ip_address_version` ASC', 'ip_address` ASC'),

    def __repr__(self):
        return self.id_network_interface


class Network_interface(Model):
    __tablename__ = 'network_interface'
    __bind_key__ = 'cmdb'

    id_network_interface = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    network_interface_name = Column(String(255), nullable=False)
    id_devices = Column(Integer, nullable=False, ForeignKey('cmdb.devices.id_devices'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    network_interface_name = Column(ASC)
    network_interface_name = Column(ASC)
    id_devices = Column(ASC, ForeignKey('cmdb.devices.id_devices'))
    id_devices = Column(ASC, ForeignKey('cmdb.devices.id_devices'))
    UniqueConstraint('', 'network_interface_name` ASC'),
    UniqueConstraint('', 'network_interface_name` ASC', 'id_devices` ASC'),

    def __repr__(self):
        return self.network_interface_name


class Operationalsystem_type(Model):
    __tablename__ = 'operationalsystem_type'
    __bind_key__ = 'cmdb'

    id_operationalsystem_type = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    description = Column(String(255), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.description


class Organization(Model):
    __tablename__ = 'organization'
    __bind_key__ = 'cmdb'

    id_organization = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    organization_name = Column(String(100), nullable=False)
    id_site = Column(Integer, nullable=False, ForeignKey('location.sites.id_sites'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None)
    organization_name = Column(ASC)
    id_site = Column(ASC, ForeignKey('location.sites.id_sites'))
    UniqueConstraint('', 'organization_name` ASC'),

    def __repr__(self):
        return self.organization_name


class Provider(Model):
    __tablename__ = 'provider'
    __bind_key__ = 'cmdb'

    id_provider = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    provider_name = Column(String(100), nullable=False)
    id_site = Column(Integer, nullable=False, ForeignKey('location.sites.id_sites'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None)
    provider_name = Column(ASC)
    id_site = Column(ASC, ForeignKey('location.sites.id_sites'))
    UniqueConstraint('', 'provider_name` ASC'),

    def __repr__(self):
        return self.provider_name


class Services(Model):
    __tablename__ = 'services'
    __bind_key__ = 'cmdb'

    id_services = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    services_name = Column(String(100), nullable=False)
    id_customers = Column(Integer, default=None, ForeignKey('cmdb.customers.id_customers'))
    id_application = Column(Integer, default=None, ForeignKey('cmdb.application.id_application'))
    services_custom_data = Column(JSON, default=None)
    services_data = Column(JSON, default=None)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    services_name = Column(ASC)
    id_customers = Column(ASC, ForeignKey('cmdb.customers.id_customers'))
    id_application = Column(ASC, ForeignKey('cmdb.application.id_application'))
    id_application = Column(ASC, ForeignKey('cmdb.application.id_application'))
    id_customers = Column(ASC, ForeignKey('cmdb.customers.id_customers'))
    UniqueConstraint('', 'services_name` ASC', 'id_customers` ASC', 'id_application` ASC'),

    def __repr__(self):
        return self.services_name


class Test(Model):
    __tablename__ = 'test'
    __bind_key__ = 'cmdb'

    id_test = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    name = Column(String(45), nullable=False)
    description = Column(String(200), nullable=False)
    action = Column(Text, nullable=False)
    test_data = Column(Text, default=None)
    cron_data = Column(Text, default=None)
    test_wait_time = Column(Integer, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.name


class Test_app_server(Model):
    __tablename__ = 'test_app_server'
    __bind_key__ = 'cmdb'

    id_test_app_server = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    id_test_title = Column(Integer, nullable=False, ForeignKey('cmdb.test_title.id_test_title'))
    id_server = Column(Integer, default=None, ForeignKey('cmdb.devices.id_devices'))
    id_application = Column(Integer, default=None, ForeignKey('cmdb.application.id_application'))
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_test_title = Column(ASC, ForeignKey('cmdb.test_title.id_test_title'))
    id_server = Column(ASC, ForeignKey('cmdb.devices.id_devices'))
    id_application = Column(ASC, ForeignKey('cmdb.application.id_application'))
    id_test_title = Column(ASC, ForeignKey('cmdb.test_title.id_test_title'))
    id_server = Column(ASC, ForeignKey('cmdb.devices.id_devices'))
    id_application = Column(ASC, ForeignKey('cmdb.application.id_application'))
    UniqueConstraint('', 'id_test_title` ASC', 'id_server` ASC', 'id_application` ASC'),

    def __repr__(self):
        return self.id_test_title


class Test_execution_control(Model):
    __tablename__ = 'test_execution_control'
    __bind_key__ = 'cmdb'

    id_test_execution_control = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    id_test = Column(Integer, nullable=False, ForeignKey('cmdb.test.id_test'))
    last_execution_time = Column(DateTime, default=None)
    nbr_execution_times = Column(Integer, default=None)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_test = Column(ASC, ForeignKey('cmdb.test.id_test'))

    def __repr__(self):
        return self.id_test


class Test_result(Model):
    __tablename__ = 'test_result'
    __bind_key__ = 'cmdb'

    id_test_result = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    id_test_status = Column(Integer, nullable=False, ForeignKey('cmdb.test_status.id_test_status'))
    id_test = Column(Integer, nullable=False)
    test_app = Column(Integer, nullable=False)
    test_server = Column(Integer, nullable=False)
    startedAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    finishedAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    duration = Column(Float(8,3), nullable=False)
    code = Column(Integer, nullable=False)
    result = Column(Text, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    id_test_status = Column(ASC, ForeignKey('cmdb.test_status.id_test_status'))

    def __repr__(self):
        return self.id_test_status


class Test_status(Model):
    __tablename__ = 'test_status'
    __bind_key__ = 'cmdb'

    id_test_status = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    name = Column(String(30), nullable=False)
    order_show = Column(Integer, default=None)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    UniqueConstraint('', 'name` ASC'),

    def __repr__(self):
        return self.name


class Test_title(Model):
    __tablename__ = 'test_title'
    __bind_key__ = 'cmdb'

    id_test_title = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    description = Column(String(255), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.description


class Test_topic(Model):
    __tablename__ = 'test_topic'
    __bind_key__ = 'cmdb'

    id_test_topic = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(200), default=None)
    id_test_title = Column(Integer, nullable=False, ForeignKey('cmdb.test_title.id_test_title'))
    execution_order = Column(Integer, nullable=False)
    id_test = Column(Integer, nullable=False, ForeignKey('cmdb.test.id_test'))
    test_order = Column(Integer, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_test_title = Column(ASC, ForeignKey('cmdb.test_title.id_test_title'))
    id_test = Column(ASC, ForeignKey('cmdb.test.id_test'))
    execution_order = Column(ASC)
    test_order = Column(ASC)
    UniqueConstraint('', 'execution_order` ASC', 'test_order` ASC'),

    def __repr__(self):
        return self.name

# Models for database: location

class Cities(Model):
    __tablename__ = 'cities'
    __bind_key__ = 'location'

    id_cities = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    city_name = Column(String(255), nullable=False)
    id_states = Column(Integer, nullable=False, ForeignKey('location.states.id_states'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    city_name = Column(ASC)
    id_states = Column(ASC, ForeignKey('location.states.id_states'))
    id_states = Column(ASC, ForeignKey('location.states.id_states'))
    UniqueConstraint('', 'city_name` ASC', 'id_states` ASC'),

    def __repr__(self):
        return self.city_name


class Country(Model):
    __tablename__ = 'country'
    __bind_key__ = 'location'

    id_country = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    country_name = Column(String(255), nullable=False)
    country_abbreviation = Column(String(5), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    country_name = Column(ASC)
    UniqueConstraint('', 'country_name` ASC'),
    UniqueConstraint('', 'country_name` ASC'),

    def __repr__(self):
        return self.country_name


class Sites(Model):
    __tablename__ = 'sites'
    __bind_key__ = 'location'

    id_sites = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    site_name = Column(String(255), nullable=False)
    id_cities = Column(Integer, nullable=False, ForeignKey('location.cities.id_cities'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    id_cities = Column(ASC, ForeignKey('location.cities.id_cities'))

    def __repr__(self):
        return self.site_name


class States(Model):
    __tablename__ = 'states'
    __bind_key__ = 'location'

    id_states = Column(Integer, primery_key=True, autoincrement=True, nullable=False)
    state_name = Column(String(255), nullable=False)
    state_abbreviation = Column(String(5), nullable=False)
    id_country = Column(Integer, nullable=False, ForeignKey('location.country.id_country'))
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.datetime.now)
    state_name = Column(ASC)
    id_country = Column(ASC, ForeignKey('location.country.id_country'))
    id_country = Column(ASC, ForeignKey('location.country.id_country'))
    UniqueConstraint('', 'state_name` ASC', 'id_country` ASC'),

    def __repr__(self):
        return self.state_name

