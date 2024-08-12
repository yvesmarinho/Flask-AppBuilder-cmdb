from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text, Index, DateTime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
import pendulum

def today_date_format():
    local_tz = pendulum.timezone('America/Sao_Paulo')
    pendulum_object = pendulum.now(local_tz)
    return pendulum_object.format('YYYY-MM-DD HH:mm:ss')

class App_type(Model):
    __bind_key__ = 'cmdb'  # Nome do banco de dados
    __tablename__ = 'app_type'  # Nome da tabela

    
    id_app_type = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    
    description = Column(String(255), nullable=False)
    
    createdAt = Column(DateTime, default=today_date_format())
    
    updatedAt = Column(DateTime, default=None, onupdate=today_date_format())
    

    

    

    

    def __repr__(self):
        return "<App_type(id_app_type={ '{' } self.id_app_type { '}' }, description={ '{' } self.description { '}' }, createdAt={ '{' } self.createdAt { '}' }, updatedAt={ '{' } self.updatedAt { '}' })>"

