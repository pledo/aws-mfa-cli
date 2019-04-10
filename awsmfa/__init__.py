#!/bin/python3

import boto3
import re
import argparse
from sys import exit
from shutil import copyfile
from os import environ, mkdir, chdir, getcwd
from jinja2 import Environment, FileSystemLoader
from os.path import isdir, exists, dirname, realpath

# -------- Argparse configuration --------------------- #

parser = argparse.ArgumentParser()

parser.add_argument('--mfa', action='store', dest='mfa_arn', required=True,
      help='Provide the mfa arn: arn:aws:iam::<aws-account-number>:mfa/<user-name>')

parser.add_argument('--region', action='store', dest='region', required=True,
                    help='Provide a aws region ex: eu-central-1, us-east-1 ...')

parser.add_argument('--profile', action='store', dest='profile', required=True,
                    help='Provide the profile ex: aws-stage, mfa-prod')

# ------------  Variables ----------------------------- #

ARGS = parser.parse_args()
AWS_CREDENTIALS_FOLDER = environ["HOME"] + "/" + ".aws"
AWS_CREDENTIALS_DESTINATION_FILE =  AWS_CREDENTIALS_FOLDER + "/"  + "credentials"
AWS_CREDENTIALS_TEMPLATE = dirname(realpath(__file__)) + "/default_template/credentials"
AWS_CREDENTIALS_TEMPLATE_FOLDER = dirname(realpath(__file__)) + "/templates"


MFA_SERIAL_NUMBER=ARGS.mfa_arn
AWS_REGION_CREDENTIALS=ARGS.region
AWS_PROFILE=ARGS.profile
MFA_PROFILE_BLOCK = "["+AWS_PROFILE+"]"+"\n"
# -------- Warning messages ---------------------------- #

WARNING_CREDENTIALS_MESSAGE = "[default]\nAWS_ACCESS_KEY_ID=< AWS_ACCESS_KEY > \
\nAWS_SECRET_ACCESS_KEY=< AWS_SECRET_ACCESS_KEY >\nAWS_DEFAULT_REGION=eu-central-1\n"


WARNING_EXPORT = "\nexport AWS_ACCESS_KEY_ID=< YOUR-ACCESS-KEYS-HERE >\
\nexport AWS_SECRET_ACCESS_KEY=< YOUR-SECRET-KEYS-HERE>\nexport \
AWS_DEFAULT_REGION=eu-central-1\n"


WARNING_AFTER_CREATED_CREDENTIALS_FILE = "The aws credentials file was created.\n\
Please put your credentials there: ~/.aws/credentials\n\nFor example: \n\n{} \n\
After that, run the aws_cli_mfa.py again"


WARNING_GREETINGS = "\n### Don't forget to export your AWS \
credentials or fill the ~/.aws/credentials file with It\n"


#--------- check_aws_credentials_file ----------------- #

def check_aws_credentials_file():
  """Checking if there is a ~/.aws/credentials file"""
  
  if isdir(AWS_CREDENTIALS_FOLDER) == False:
    mkdir(AWS_CREDENTIALS_FOLDER)
    copyfile(AWS_CREDENTIALS_TEMPLATE, AWS_CREDENTIALS_DESTINATION_FILE)

    print(WARNING_GREETINGS + "\n" + WARNING_EXPORT + "\n" + 
       WARNING_AFTER_CREATED_CREDENTIALS_FILE.format(WARNING_CREDENTIALS_MESSAGE))
    exit(0)

  elif exists(AWS_CREDENTIALS_DESTINATION_FILE) == False:
    copyfile(AWS_CREDENTIALS_TEMPLATE, AWS_CREDENTIALS_DESTINATION_FILE)
    
    print(WARNING_GREETINGS + "\n" + WARNING_EXPORT + "\n" + 
       WARNING_AFTER_CREATED_CREDENTIALS_FILE.format(WARNING_CREDENTIALS_MESSAGE))
    exit(0)

# -------- Getting temporary credentials -------------- #

dest_config_file = AWS_CREDENTIALS_DESTINATION_FILE

def get_temp_credentials():
  """ Getting temporary credentials """

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
  temp_credentials["PROFILE"] =  AWS_PROFILE

  return(temp_credentials)

# -------- Configuring the temporary credentials ------ #

def configuring_temporary_credentials(temp_credentials):
  """ Configuring the .aws/credentials """

  template_dir = 'templates'

  file_loader = FileSystemLoader(AWS_CREDENTIALS_TEMPLATE_FOLDER)
  env = Environment(loader=file_loader)

  template_file_name = file_loader.list_templates()[0]
  template = env.get_template(template_file_name)

  output = template.render(credentials=temp_credentials)

  with open(dest_config_file, "a") as f:
       f.write(output)

# -------- Cleaning the config file ------------------- #

def cleaning_config_file(lines):
  """ Cleaning the config file"""

  mfa_index = lines.index(MFA_PROFILE_BLOCK)
  mfa_end_index = mfa_index + 5

  start_lines = lines[:mfa_index]
  
  end_lines = lines[mfa_end_index:]
  lines = start_lines + end_lines
  
  # Call the formating function organize
  #lines = formating_config_file(lines)ß
  
  with open(dest_config_file, "w") as f:
       f.writelines(lines)

# -------- Formating the config file ------------------- #
def formating_config_file(lines):
  """ Formating the config file at the end of the process """
  blocks_start = []
  pattern = r"\[.*?\]\n"
  for line in lines:
      match = re.match(pattern, line)
      if match:
          blocks_start.append(match.string)
  #print(blocks_start)
  blocks_start.remove(blocks_start[0])
  
  for block in blocks_start:
    block_index = lines.index(block)
    before_block = block_index - 1
    if lines[before_block] != '\n':
      lines.insert(before_block, '\n')

  #print("Last element: {}".format(lines[-1]))
  #if lines[-1] != '\n':
  #  lines.append('\n')

  #print("List formatted: {}".format(lines))
  return(lines)

# -------- Main function   ----------------------------- #

def main():
  check_aws_credentials_file()

  with open(dest_config_file, "r") as file:
    lines = file.readlines()
    #print("Lines: {}".format(lines))

  if MFA_PROFILE_BLOCK in lines:
    cleaning_config_file(lines)

  temp_credentials = get_temp_credentials()
  configuring_temporary_credentials(temp_credentials)

#------------------------------------------------------ #

if __name__ == "__main__":
  main()
