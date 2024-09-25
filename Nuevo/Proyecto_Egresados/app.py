import control
from model import config

ctr = control

if __name__ == '__main__':
    ctr.app.config.from_object(config['development'])
    #ctr.app.register_error_handler(404, Error404)
    ctr.app.run()