class Config:
    SECRET_KEY ='406811fdec26fb2c0bd5f1ac17c5f1362f845eb63125e097'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '2i6a'
    MYSQL_DB = 'seg_egresados5'
    


config = {
    'development': DevelopmentConfig
}