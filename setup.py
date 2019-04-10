from setuptools import setup, find_packages

setup(
    name='aws-mfa-cli',
    version='0.1.0',
    description='Easily configure the temporary credentials',
    long_description='Get temporary credentials and put it on ~/.aws/credentials',
    long_description_content_type='text/markdown',
    license='MIT',
    author='Paulo Ledo',
    author_email='paulofledo@gmail.com',
    packages=find_packages(),
    package_data={'awsmfa': ['default_template/credentials', 'templates/credentials']},
    scripts=['aws-mfa-cli'],
    entry_points={
        'console_scripts': [
            'aws-mfa-cli=awsmfa:main',
        ],
    },
    url='https://github.com/pledo/aws-mfa-cli',
    install_requires=['boto3', 'jinja2'],
    include_package_data=True

)
