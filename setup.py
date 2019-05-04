from setuptools import setup

setup(
    name='chatroom',
    version='0.0.1',
    description='simple python wss chatroom',
    author='Rio Lin',
    author_email='pinhuilin86@gmail.com',
    url='https://github.com/riorz/wss_chat',
    package=['chatroom'],
    install_requires=['websockets', 'blessed'],
    entry_points={
        'console_scripts': [
            'chatroom = chatroom.scripts.command_line:main',
        ],
    },
)
