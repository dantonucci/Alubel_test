from db import db
from influxdb import InfluxDBClient

# create USER 
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
  
  
# Models to create tabel of credentials for TimeSeries Database
class InfluxDB(db.Model):
    __tablename__ = 'DB_credentials'
    
    Project_ID = db.Column(db.INTEGER, primary_key=True)
    Project_name = db.Column(db.String(100), nullable=False)
    host_DB = db.Column(db.String(40), nullable=False)
    port_DB = db.Column(db.Integer, nullable=False)
    username_DB = db.Column(db.String(50), nullable=False)
    password_DB = db.Column(db.String(50), nullable=False)
    database_DB = db.Column(db.String(50), nullable=False)
    
    def __init__(self, Project_name, host_DB, port_DB,
                 username_DB,password_DB,database_DB):
        self.Project_name = Project_name
        self.host_DB = host_DB
        self.port_DB = port_DB
        self.username_DB = username_DB
        self.password_DB = password_DB
        self.database_DB = database_DB
        
    def json(self):
        return {
            'Project_name': self.Project_name,
            'host_DB': self.host_DB,
            'port_DB': self.port_DB,
            'username_DB': self.username_DB,
            'password_DB': self.password_DB,
            'database_DB': self.database_DB 
        }
        
    @classmethod
    def find_database(cls, Project_name):
        return cls.query.filter_by(Project_name=Project_name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def db_connection(cls, Project_name):#,query):
        Credentials = cls.query.filter_by(Project_name=Project_name).first()
        Client = InfluxDBClient(
            host =  Credentials.host_DB,
            port = Credentials.port_DB,
            username = Credentials.username_DB,
            password= Credentials.password_DB,
            database = Credentials.database_DB,
            ssl = True,
            verify_ssl= True
        )
        
        # ResultQuery = Client.query(query)
        
        # return (ResultQuery)
        return(Client)
    
    @classmethod    
    def Get_DB_Info(cls, Project_name):
        return cls.query.filter_by(Project_name=Project_name).first()
        
# class DataFromSystem(db.Model):
#     def __init__(self):