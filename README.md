## Usage:

1- Clone the project and enter into the project's folder.
```
 $ git clone  https://github.com/pledo/aws-mfa-cli.git ; cd aws-mfa-cli
```

2- Configure your ~/.aws/credentials with your keys and region, for example:
```
~/.aws.credentials:

[default]
AWS_ACCESS_KEY_ID=< AWS_ACCESS_KEY >
AWS_SECRET_ACCESS_KEY=< AWS_SECRET_ACCESS_KEY >
AWS_DEFAULT_REGION=us-east-1
```
Or export your keys, running this line in your terminal

```
$ export AWS_ACCESS_KEY_ID=<Your-Keys-Here> ; export AWS_SECRET_ACCESS_KEY=<Your-Keys-Here> ; export AWS_DEFAULT_REGION=<AWS-Region-Here>
```

3- Run the command providing your mfa arn and region

```
$ python3 aws_cli_mfa.py --mfa arn:aws:iam::<Account-Number>:mfa/<Your-User-Name> --region=us-east-1
```

4- Check your ~/.aws/credentials, It should have a profile block like that:
```
[default]
Here should have your default configuration.
THe script will just create the [mfa] block

[mfa]
AWS_ACCESS_KEY_ID=< With the temporary key >
AWS_SECRET_ACCESS_KEY=<...>
AWS_SESSION_TOKEN=<...>
AWS_DEFAULT_REGION=<...>
```

5- Test the aws cli with the mfa profile, for example:

```
$ aws --profile mfa s3 ls
```

RoadMap

x- Remove only the [mfa] block, keep everything after. 
x- Create a description for README explaing the script. 
x- Create the cli option for mfa arn and other most important options. 
- Take the aws region from the environment variable: AWS_DEFAULT_REGION, if it exists. 
- Take the aws region from aws/credentials file: AWS_DEFAULT_REGION, if it exists. 
- Tests
- Instalation config