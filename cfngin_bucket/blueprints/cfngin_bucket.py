"""Creates an S3 Bucket for CFNgin.

Variables
---------

**BucketName (Optional[str])**
    Name to use for the S3 Bucket. If not provided, the name will be
    ``<stack-name>-<region>``. (`default:` ``None``)

**KMSMasterKeyID (Optional[str])**
    Key ID or ARN for a KMS key to use for ServerSideEncryptionByDefault_.
    If not provided, the default S3 service key will be used.
    (`default:` ``None``)

**Tags (Dict[str, str])**
    Mapping for {tag-key: tag-value} for the Bucket. (`default:` ``{}``)

.. _ServerSideEncryptionByDefault: https://tinyurl.com/vub9cej

Outputs
-------

**CFNginBucket (str)**
    Name of the S3 Bucket that was created.

**CFNginBucketArn (str)**
    ARN of the S3 Bucket that was created.

"""
from typing import Any, Dict

from runway.cfngin.blueprints.base import Blueprint
from troposphere import GetAtt, Tags, Template, s3

TEMPLATE_DESCRIPTION = 'Runway CFNgin Bucket'


class BlueprintClass(Blueprint):
    """Extends CFNgin's Blueprint class."""

    VARIABLES: Dict[str, Any] = {
        'BucketName': {'type': (str, type(None)), 'default': None},
        'KMSMasterKeyID': {'type': (str, type(None)), 'default': None},
        'Tags': {'type': dict, 'default': {}}
    }

    @property
    def bucket_name(self) -> str:
        """CFNgin Bucket name."""
        if self.vars['BucketName']:
            return self.vars['BucketName']
        # using 'bucket_region' for the time being until there is something more reliable
        return f"{self.name.lower()}-{self.context.bucket_region}"

    @property
    def vars(self) -> Dict[str, Any]:
        """Blueprint variables.

        Returns:
            Resolved variables.

        """
        return self.get_variables()

    def bucket(self) -> s3.Bucket:
        """CFNgin Bucket resource."""
        return s3.Bucket(
            'CFNginBucket',
            BucketEncryption=self.encryption_settings(),
            BucketName=self.bucket_name,
            Tags=Tags(**self.vars['Tags']),
            # not parameterized b/c this shouldn't need to be paused
            VersioningConfiguration=s3.VersioningConfiguration(Status='Enabled')
        )

    def encryption_settings(self,
                            kms_key_id: str = None
                            ) -> s3.BucketEncryption:
        """CFNgin Bucket encryption settings.

        Args:
            kms_key_id: Key ID or ARN for a KMS key to use for default Bucket
                encryption. The default S3 service key will be used if not
                provided.

        Returns:
            S3 Bucket encryption settings.

        """
        kwargs = {'SSEAlgorithm': 'AES256'}
        if not kms_key_id:
            kms_key_id = self.vars['KMSMasterKeyID']
        if kms_key_id:
            kwargs = {'KMSMasterKeyID': kms_key_id,
                      'SSEAlgorithm': 'aws:kms'}
        return s3.BucketEncryption(
            ServerSideEncryptionConfiguration=[s3.ServerSideEncryptionRule(
                ServerSideEncryptionByDefault=s3.ServerSideEncryptionByDefault(
                    **kwargs))])

    def create_template(self) -> None:
        """Create template (method called by CFNgin)."""
        template: Template = self.template
        template.set_description(TEMPLATE_DESCRIPTION)
        template.set_version('2010-09-09')

        bucket = template.add_resource(self.bucket())

        self.add_output(bucket.title, bucket.ref())
        self.add_output(f'{bucket.title}Arn', GetAtt(bucket, 'Arn'))
