from app import app
import flask_migrate
import fire
import views


def run_server():
    app.run()


def migrate_init():
    with app.app_context():
        return flask_migrate.init('migrates')


def migrate(msg):
    with app.app_context():
        return flask_migrate.migrate('migrates', message=msg)


def upgrade(revision='head'):
    with app.app_context():
        return flask_migrate.upgrade('migrates', revision)


def downgrade(revision='-1'):
    with app.app_context():
        return flask_migrate.downgrade('migrates', revision)


if __name__ == '__main__':
    fire.Fire({
        'run_server': run_server,
        'migrate_init': migrate_init,
        'migrate': migrate,
        'downgrade': downgrade,
        'upgrade': upgrade
    })