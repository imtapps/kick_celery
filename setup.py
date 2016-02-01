from setuptools import setup


setup(
    name='kick_celery',
    version='0.0.8',
    author='imtapps',
    description='Kicks Celery',
    install_requires=['paramiko'],
    py_modules=['kick_celery'],
    entry_points={
        'console_scripts': {
            'kick_celery = kick_celery:main'
        }
    }
)
