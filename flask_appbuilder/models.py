
import logging
from flask_sqlalchemy import SQLAlchemy

# Configuração do logging
logging = logging.getLogger(__name__)

try:
    db = SQLAlchemy()


    class App_type(db.Model):
        __tablename__ = 'app_type'
        
        id_app_type = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        description = db.Column(db.VARCHAR(255), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Application(db.Model):
        __tablename__ = 'application'
        
        id_application = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        name = db.Column(db.VARCHAR(255), nullable=False, )
        
        version = db.Column(db.VARCHAR(50), nullable=True, )
        
        id_app_type = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_app_type = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Customers(db.Model):
        __tablename__ = 'customers'
        
        id_customers = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        customers_name = db.Column(db.VARCHAR(100), nullable=False, )
        
        id_organization = db.Column(db.INT, nullable=False, )
        
        id_site = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        customers_name = db.Column(db.ASC, nullable=True, )
        
        id_site = db.Column(db.ASC, nullable=True, )
        
        id_organization = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Device_app_dns(db.Model):
        __tablename__ = 'device_app_dns'
        
        id_device = db.Column(db.INT, nullable=False, )
        
        id_dns = db.Column(db.INT, nullable=False, )
        
        id_application = db.Column(db.INT, nullable=False, )
        
        app_port = db.Column(db.INT, nullable=False, )
        
        server_ip_type = db.Column(db.ENUM, nullable=True, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_dns = db.Column(db.ASC, nullable=True, )
        
        id_device = db.Column(db.ASC, nullable=True, )
        
        id_application = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Device_type(db.Model):
        __tablename__ = 'device_type'
        
        id_device_type = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        description = db.Column(db.VARCHAR(255), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Devices(db.Model):
        __tablename__ = 'devices'
        
        id_devices = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        id_device_type = db.Column(db.INT, nullable=False, )
        
        device_name = db.Column(db.VARCHAR(255), nullable=False, )
        
        id_operational_system = db.Column(db.INT, nullable=False, )
        
        id_provider = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_device_type = db.Column(db.ASC, nullable=True, )
        
        id_operational_system = db.Column(db.ASC, nullable=True, )
        
        id_provider = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Dns_a_register(db.Model):
        __tablename__ = 'dns_a_register'
        
        id_dns_a_register = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        name = db.Column(db.VARCHAR(256), nullable=False, )
        
        comment = db.Column(db.TEXT, nullable=True, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Ip_address(db.Model):
        __tablename__ = 'ip_address'
        
        id_ip_address = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        id_network_interface = db.Column(db.INT, nullable=False, )
        
        ip_address_name = db.Column(db.VARCHAR(255), nullable=False, )
        
        ip_address_type = db.Column(db.ENUM, nullable=True, )
        
        ip_address_version = db.Column(db.ENUM, nullable=True, )
        
        ip_address = db.Column(db.VARCHAR(50), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_network_interface = db.Column(db.ASC, nullable=True, )
        
        ip_address_type = db.Column(db.ASC, nullable=True, )
        
        ip_address_version = db.Column(db.ASC, nullable=True, )
        
        ip_address = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Network_interface(db.Model):
        __tablename__ = 'network_interface'
        
        id_network_interface = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        network_interface_name = db.Column(db.VARCHAR(255), nullable=False, )
        
        id_devices = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        network_interface_name = db.Column(db.ASC, nullable=True, )
        
        network_interface_name = db.Column(db.ASC, nullable=True, )
        
        id_devices = db.Column(db.ASC, nullable=True, )
        
        id_devices = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Operationalsystem_type(db.Model):
        __tablename__ = 'operationalsystem_type'
        
        id_operationalsystem_type = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        description = db.Column(db.VARCHAR(255), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Organization(db.Model):
        __tablename__ = 'organization'
        
        id_organization = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        organization_name = db.Column(db.VARCHAR(100), nullable=False, )
        
        id_site = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        organization_name = db.Column(db.ASC, nullable=True, )
        
        id_site = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Provider(db.Model):
        __tablename__ = 'provider'
        
        id_provider = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        provider_name = db.Column(db.VARCHAR(100), nullable=False, )
        
        id_site = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        provider_name = db.Column(db.ASC, nullable=True, )
        
        id_site = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Services(db.Model):
        __tablename__ = 'services'
        
        id_services = db.Column(db.INT(11), autoincrement=True, nullable=False, )
        
        services_name = db.Column(db.VARCHAR(100), nullable=False, )
        
        id_customers = db.Column(db.INT(11), nullable=True, )
        
        id_application = db.Column(db.INT(11), nullable=True, )
        
        services_custom_data = db.Column(db.JSON, nullable=True, )
        
        services_data = db.Column(db.JSON, nullable=True, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        services_name = db.Column(db.ASC, nullable=True, )
        
        id_customers = db.Column(db.ASC, nullable=True, )
        
        id_application = db.Column(db.ASC, nullable=True, )
        
        id_application = db.Column(db.ASC, nullable=True, )
        
        id_customers = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test(db.Model):
        __tablename__ = 'test'
        
        id_test = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        name = db.Column(db.VARCHAR(45), nullable=False, )
        
        description = db.Column(db.VARCHAR(200), nullable=False, )
        
        action = db.Column(db.TEXT, nullable=False, )
        
        test_data = db.Column(db.TEXT, nullable=True, )
        
        cron_data = db.Column(db.TEXT, nullable=True, )
        
        test_wait_time = db.Column(db.INT(5), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test_app_server(db.Model):
        __tablename__ = 'test_app_server'
        
        id_test_app_server = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        id_test_title = db.Column(db.INT, nullable=False, )
        
        id_server = db.Column(db.INT(11), nullable=True, )
        
        id_application = db.Column(db.INT(11), nullable=True, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_test_title = db.Column(db.ASC, nullable=True, )
        
        id_server = db.Column(db.ASC, nullable=True, )
        
        id_application = db.Column(db.ASC, nullable=True, )
        
        id_test_title = db.Column(db.ASC, nullable=True, )
        
        id_server = db.Column(db.ASC, nullable=True, )
        
        id_application = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test_execution_control(db.Model):
        __tablename__ = 'test_execution_control'
        
        id_test_execution_control = db.Column(db.INT(11), autoincrement=True, nullable=False, )
        
        id_test = db.Column(db.INT(11), nullable=False, )
        
        last_execution_time = db.Column(db.DATETIME, nullable=True, )
        
        nbr_execution_times = db.Column(db.INT, nullable=True, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_test = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test_result(db.Model):
        __tablename__ = 'test_result'
        
        id_test_result = db.Column(db.INT(11), autoincrement=True, nullable=False, )
        
        id_test_status = db.Column(db.INT(11), nullable=False, )
        
        id_test = db.Column(db.INT(11), nullable=False, )
        
        test_app = db.Column(db.INT(11), nullable=False, )
        
        test_server = db.Column(db.INT(11), nullable=False, )
        
        startedAt = db.Column(db.DATETIME, nullable=False, )
        
        finishedAt = db.Column(db.DATETIME, nullable=False, )
        
        duration = db.Column(db.DECIMAL(8,3), nullable=False, )
        
        code = db.Column(db.INT(11), nullable=False, )
        
        result = db.Column(db.TEXT(255), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=False, )
        
        id_test_status = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test_status(db.Model):
        __tablename__ = 'test_status'
        
        id_test_status = db.Column(db.INT(11), autoincrement=True, nullable=False, )
        
        name = db.Column(db.VARCHAR(30), nullable=False, )
        
        order_show = db.Column(db.INT(11), nullable=True, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test_title(db.Model):
        __tablename__ = 'test_title'
        
        id_test_title = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        description = db.Column(db.VARCHAR(255), nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    
    class Test_topic(db.Model):
        __tablename__ = 'test_topic'
        
        id_test_topic = db.Column(db.INT, autoincrement=True, nullable=False, )
        
        name = db.Column(db.VARCHAR(100), nullable=False, )
        
        description = db.Column(db.VARCHAR(200), nullable=True, )
        
        id_test_title = db.Column(db.INT(11), nullable=False, )
        
        execution_order = db.Column(db.INT, nullable=False, )
        
        id_test = db.Column(db.INT, nullable=False, )
        
        test_order = db.Column(db.INT, nullable=False, )
        
        createdAt = db.Column(db.DATETIME, nullable=True, )
        
        updatedAt = db.Column(db.DATETIME, nullable=True, )
        
        id_test_title = db.Column(db.ASC, nullable=True, )
        
        id_test = db.Column(db.ASC, nullable=True, )
        
        execution_order = db.Column(db.ASC, nullable=True, )
        
        test_order = db.Column(db.ASC, nullable=True, )
        

    logging.info("Modelos criados com sucesso.")
    

except Exception as e:
    logging.error("Erro ao criar os modelos: %s", e)
    raise