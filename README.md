## Usage:

1- Clone the project and enter into the project's folder.
```
 $ git clone  https://github.com/pledo/aws-mfa-cli.git ; cd aws-mfa-cli
```

2- Intall the command cli
```
$ python3 setup.py install
```

3- Configure your ~/.aws/credentials with your keys and region, for example:
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

4- Run the command providing your mfa arn and region

```
$ aws-mfa-cli --mfa arn:aws:iam::<Account-Number>:mfa/<Your-User-Name> --region=us-east-1 --profile mfa-dev
```

5- Check your ~/.aws/credentials, It should have a profile block like that:
```
[default]
Here should have your default configuration.
THe script will just create the [mfa] block

[mfa-dev] **here could be: mfa-stage for example**
AWS_ACCESS_KEY_ID=< With the temporary key >
AWS_SECRET_ACCESS_KEY=<...>
AWS_SESSION_TOKEN=<...>
AWS_DEFAULT_REGION=<...>
```

6- Test the aws cli with the mfa profile, for example:

```
$ aws --profile mfa-dev s3 ls
```

RoadMap:

x-Instalation config
x-Remove only the [mfa] block, keep everything after. 
x-Create a description for README explaing the script. 
x-Create the cli option for mfa arn and other most important options. 

- Take the aws region from the env variable: AWS_DEFAULT_REGION, if it exists. 
- Take the aws region from aws/credentials file: AWS_DEFAULT_REGION, if it exists. 
- Tests
- Profile: mfa-dev, mfa-stage
