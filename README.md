## Usage:

1- Install an MFA app in your Android or iPhone, my suggestion is https://authy.com/

2- After that, you should enable the MFA for your IAM user:
   https://www.youtube.com/watch?v=A3AObXBJ4Lw 

3- Clone the project and enter into the project's folder.
```
 $ git clone  https://github.com/pledo/aws-mfa-cli.git ; cd aws-mfa-cli
```

4- Install the command cli
```
$ python3 setup.py install
```

5- Configure your ~/.aws/credentials with your keys and region, for example:
```
~/.aws.credentials:

[default] # you can use a profile for example: [production] instead of [defatul]
AWS_ACCESS_KEY_ID=< AWS_ACCESS_KEY >
AWS_SECRET_ACCESS_KEY=< AWS_SECRET_ACCESS_KEY >
AWS_DEFAULT_REGION=us-east-1
```
Or export your keys, running this line in your terminal

```
$ export AWS_ACCESS_KEY_ID=<Your-Keys-Here> ; export AWS_SECRET_ACCESS_KEY=<Your-Keys-Here> ; export AWS_DEFAULT_REGION=us-east-1
```

Or you can export the profile you are using to access the AWS account, for example, if in your ~/.aws/credentials  your have a profile
called [aws-prod] you can run:

```
$export AWS_PROFILE=aws-prod
```


6- Run the command providing your mfa arn and region.

```
$ aws-mfa-cli --mfa arn:aws:iam::<AccountNumber>:mfa/<Your-User-Name> --region=eu-central-1 --profile mfa-prod
```

7- Check your ~/.aws/credentials, It should have a profile block like that:
```
[default]
Here should have your default configuration.
THe script will just create the [mfa] block

[mfa-prod] **here could be: mfa-stage for example**
AWS_ACCESS_KEY_ID=< With the temporary key >
AWS_SECRET_ACCESS_KEY=<...>
AWS_SESSION_TOKEN=<...>
AWS_DEFAULT_REGION=<...>
```

8- Test the aws cli with the mfa profile, for example:

```
$ aws --profile mfa-prod s3 ls
```
or you can export the mfa-prod profile and remove the --profile from the aws cli

```
$ export AWS_PRODILE=mfa-prod
$ aws s3 ls
```

If you would like to uninstall the aws-mfa-cli just run:

```
$ pip3 uninstall aws-mfa-cli
```

RoadMap:

x-Installation config
x-Remove only the [mfa] block, keep everything after. 
x-Create a description for README explaining the script. 
x-Create the cli option for mfa arn and other most important options. 

- Take the aws region from the env variable: AWS_DEFAULT_REGION, if it exists. 
- Take the aws region from aws/credentials file: AWS_DEFAULT_REGION, if it exists. 
- Tests
x- Multiple profiles: mfa-dev, mfa-stage

- Organize the mfa- blocks with always one line between blocks
