# cfngin-bucket

[![CI/CD](https://github.com/cfngin/cfngin-bucket/workflows/CI/CD/badge.svg)](https://github.com/cfngin/cfngin-bucket/actions?query=workflow%3ACI%2FCD)

Blueprint for creating a CFNgin bucket.

## Requirements

- python_version >= 3.7
- runway >= 1.4.4

## Usage

```yaml
variables:
  namespace: example

deployments:
  - modules:
      - path: git::git://github.com/cfngin/cfngin-bucket.git?tag=v0.1.0
        type: cloudformation
        parameters:
          BucketName: ${var namespace}-${env DEPLOY_ENVIRONMENT}-${env AWS_REGION}
          Tags: {}  # if no tags need to be added, provide an empty mapping
    parameters:
      namespace: ${var namespace}
```

## Parameters

- **BucketName (Optional[str]):** Name to use for the S3 Bucket. If not provided, the name will be `<stack-name>-<region>`. (*default:* `None`)
- **KMSMasterKeyID (Optional[str]):** Key ID or ARN for a KMS key to use for [ServerSideEncryptionByDefault]. If not provided, the default S3 service key will be used. (*default:* `None`)
- **namespace (str):** [CFNgin namespace] used to prefix the stack name and default resource names.
- **Tags (Dict[str, str]):** Mapping for {tag-key: tag-value} for the Bucket. (*default:* `{}`)

## Outputs

- **CFNginBucket (str):** Name of the S3 Bucket that was created.
- **CFNginBucketArn (str):** ARN of the S3 Bucket that was created.


[CFNgin namespace]: https://docs.onica.com/projects/runway/en/release/cfngin/config.html#namespace
[ServerSideEncryptionByDefault]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html
