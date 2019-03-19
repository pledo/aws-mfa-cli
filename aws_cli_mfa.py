#!/bin/python3
import argparse
import boto3
from jinja2 import Environment, FileSystemLoader
from os import environ, mkdir, chdir, getcwd
from os.path import isdir, exists, dirname, realpath
from shutil import copyfile
from sys import exit

# ----------------------------------------- #
parser = argparse.ArgumentParser()

parser.add_argument('--mfa', action='store', dest='mfa_arn', required=True,
                    help='Provide the mfa arn: arn:aws:iam::<aws-account-number>:mfa/<user-name>')

parser.add_argument('--region', action='store', dest='region', required=True,
                    help='Provide a aws region ex: eu-central-1, us-east-1 ...')


# ------------  Environments ------------ #

ARGS = parser.parse_args()
AWS_CREDENTIALS_FOLDER = environ["HOME"] + "/" + ".aws"
AWS_CREDENTIALS_DESTINATION_FILE =  AWS_CREDENTIALS_FOLDER + "/"  + "credentials"
AWS_CREDENTIALS_TEMPLATE = dirname(realpath(__file__)) + "/default_template/credentials"
AWS_CREDENTIALS_TEMPLATE_FOLDER = dirname(realpath(__file__)) + "/templates"


MFA_SERIAL_NUMBER=ARGS.mfa_arn
AWS_REGION_CREDENTIALS=ARGS.region

# ----------------------------------------- #
# Warning messages

WARNING_CREDENTIALS_MESSAGE = "[default]\nAWS_ACCESS_KEY_ID=< AWS_ACCESS_KEY > \
  \nAWS_SECRET_ACCESS_KEY=< AWS_SECRET_ACCESS_KEY >\nAWS_DEFAULT_REGION=eu-central-1\n"


WARNING_EXPORT = "\nexport AWS_ACCESS_KEY_ID=< YOUR-ACCESS-KEYS-HERE >\
  \nexport AWS_SECRET_ACCESS_KEY=< YOUR-SECRET-KEYS-HERE>\nexport AWS_DEFAULT_REGION=eu-central-1\n"


WARNING_AFTER_CREATED_CREDENTIALS_FILE = "The aws credentials file was created.\nPlease put your credentials there:\
  ~/.aws/credentials\n\nFor example: \n\n{} \nAfter that, run the aws_cli_mfa.py again"


WARNING_GREETINGS = "\n### Don't forget to export your AWS credentials or fill the ~/.aws/credentials file with It\n"

 #----------------------------------------- #

def check_aws_credentials_file():
  """Checking if there is a ~/.aws/credentials file"""
  #print("\n### Running check_aws_credentials_file function ###\n")

  if isdir(AWS_CREDENTIALS_FOLDER) == False:
    mkdir(AWS_CREDENTIALS_FOLDER)
    copyfile(AWS_CREDENTIALS_TEMPLATE, AWS_CREDENTIALS_DESTINATION_FILE)

    print(WARNING_GREETINGS)
    print(WARNING_EXPORT)
    print(WARNING_AFTER_CREATED_CREDENTIALS_FILE.format(WARNING_CREDENTIALS_MESSAGE))

    exit(0)

  elif exists(AWS_CREDENTIALS_DESTINATION_FILE) == False:
    copyfile(AWS_CREDENTIALS_TEMPLATE, AWS_CREDENTIALS_DESTINATION_FILE)
    
    print(WARNING_GREETINGS)
    print(WARNING_EXPORT)
    print(WARNING_AFTER_CREATED_CREDENTIALS_FILE.format(WARNING_CREDENTIALS_MESSAGE))

    exit(0)

# ----------------------------------------- #

#dest_config_file = '.aws/credentials'
dest_config_file = AWS_CREDENTIALS_DESTINATION_FILE

def get_temp_credentials():
  # Prompt for MFA time-based one-time password (TOTP)
  mfa_TOTP = input("Enter the MFA code: ")

  client = boto3.client('sts')

  tempCredentials = client.get_session_token(
      SerialNumber=MFA_SERIAL_NUMBER,
      TokenCode=mfa_TOTP
  )

  temp_credentials = {}
  raw_temp_credentials = tempCredentials["Credentials"]
  temp_credentials["AWS_ACCESS_KEY"] = raw_temp_credentials["AccessKeyId"]
  temp_credentials["AWS_SECRET_ACCESS_KEY"] = raw_temp_credentials["SecretAccessKey"]
  temp_credentials["SESSION_TOKEN"] = raw_temp_credentials["SessionToken"]
  temp_credentials["AWS_REGION"] =  AWS_REGION_CREDENTIALS
  #print(temp_credentials)
  return(temp_credentials)


def configuring_temporary_credentials(temp_credentials):
  """ Configuring the .aws/credentials """
  #print(" Running the configuring_temporary_credentials function ")

  #template_dir = AWS_CREDENTIALS_TEMPLATE_FOLDER
  template_dir = 'templates'

  # Destination config file, usually = .aws/credentials
  #print(AWS_CREDENTIALS_TEMPLATE_FOLDER)
  file_loader = FileSystemLoader(AWS_CREDENTIALS_TEMPLATE_FOLDER)
  env = Environment(loader=file_loader)

  #print("\n ### Template files:{}###\n".format(file_loader.list_templates()))

  template_file_name = file_loader.list_templates()[0]
  template = env.get_template(template_file_name)

  output = template.render(credentials=temp_credentials)
  with open(dest_config_file, "a") as f:
       f.write(output)

def cleaning_config_file(lines):
  """ Cleaning the config file"""

  mfa_index = lines.index("[mfa]\n")
  mfa_end_index = mfa_index + 5

  start_lines = lines[:mfa_index]
  
  end_lines = lines[mfa_end_index:]
  lines = start_lines + end_lines
  with open(dest_config_file, "w") as f:
       f.writelines(lines)

# ----------------------------------------

def main():
  check_aws_credentials_file()

  with open(dest_config_file, "r") as file:
    lines = file.readlines()

  if '[mfa]\n' in lines:
    #print("Let's clean the .aws/credentials")
    cleaning_config_file(lines)
  temp_credentials = get_temp_credentials()
  configuring_temporary_credentials(temp_credentials)

#----------------------------------------
if __name__ == "__main__":
  main()