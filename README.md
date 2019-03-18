##Usage:

1- CLone the project
```
 $git clone  https://github.com/pledo/aws-mfa-cli.git
```

2-  Configure your ~/.aws/credentials with your keys and region, for example:
```
~/.aws.credentials:

[default]
AWS_ACCESS_KEY_ID=< AWS_ACCESS_KEY >
AWS_SECRET_ACCESS_KEY=< AWS_SECRET_ACCESS_KEY >
AWS_DEFAULT_REGION=us-east-1
```
Or export your keys, running this line in your terminal

```
$ export AWS_ACCESS_KEY_ID=AKASDASDASDASD ; export AWS_SECRET_ACCESS_KEY=HzS/ASDASDASDSADASDQWEQWEQWEQWE ; export AWS_DEFAULT_REGION=us-east-1
```

3- Run the command providing your mfa arn and region

```
$ python3 aws_cli_mfa.py --mfa arn:aws:iam::006033402816:mfa/devops_test --region=eu-central-2
```

4- Now Check your ~/.aws/credentials, It should have a profile block like that:
```
[mfa]
AWS_ACCESS_KEY_ID=< With the temporary key >
AWS_SECRET_ACCESS_KEY=<...>
AWS_SESSION_TOKEN=<...>
AWS_DEFAULT_REGION=<...>
```

RoadMap

- Remove only the [mfa] block, keep everything after
- Create a description for README explaing the script
- Create the cli option for mfa arn and other most important options.
- Take the aws region from the environment variable: AWS_DEFAULT_REGION, if it exist.
