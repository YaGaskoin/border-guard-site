class Conf(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/pogran'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ключ'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'login'
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_INPUT_NAME = 'files'
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
    DROPZONE_MAX_FILE_EXCEED = 10
    DROPZONE_DEFAULT_MESSAGE = 'Перетащите файлы сюда'
    DROPZONE_PARALLEL_UPLOADS = 0
    WHOOSH_BASE = 'whoosh'


UPLOAD_FOLDER = 'static/images'
rusWeekDays = ['Пн.', 'Вт.', 'Ср.', 'Чт.', 'Пт.', 'Сб.', 'Вс.']
rusMonths = ['Янв.', 'Фев.', 'Март',  'Апр.',  'Май',  'Июнь',  'Июль',  'Авг.',  'Сент.',  'Окт.',  'Нояб.',  'Дек.']