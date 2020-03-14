"""S3 resources for this CFNgin module."""
from typing import Any, Dict

from runway.cfngin.context import Context
from troposphere import Output, Tags, Template, s3


class CFNginBucket(s3.Bucket):
    """S3 Bucket used for CFNgin caching.

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
        Mapping of {tag-key: tag-value} for the Bucket. (`default:` ``{}``)

    .. _ServerSideEncryptionByDefault: https://tinyurl.com/vub9cej

    Outputs
    -------

    **CFNginBucket (str)**
        Name of the S3 Bucket that was created.

    **CFNginBucketArn (str)**
        ARN of the S3 Bucket that was created.

    """

    LOGICAL_NAME = 'CFNginBucket'
    VARIABLES: Dict[str, Any] = {
        'BucketName': {'type': (str, type(None)), 'default': None},
        'KMSMasterKeyID': {'type': (str, type(None)), 'default': None},
        'Tags': {'type': dict, 'default': {}}
    }

    def __init__(self, *,
                 context: Context,
                 stack_fqn: str,
                 template: Template,
                 variables: Dict[str, Any],
                 **kwargs: Any) -> None:
        """Instantiate class.

        Keyword Args:
            context: CFNgin context object.
            stack_fqn: Fully qualified name of the Stack this resource is
                being created in.
            template: Troposphere template object.
            variables: Resolved CFNgin variables from a Blueprint.

        """
        self._context = context
        self._vars = variables
        self._stack_fqn = stack_fqn

        super().__init__(title=self.LOGICAL_NAME,
                         template=template,
                         BucketEncryption=self._get_encryption_settings(),
                         BucketName=self._get_bucket_name(),
                         Tags=Tags(**self._vars.get('Tags', {})),
                         VersioningConfiguration=s3.VersioningConfiguration(
                             Status='Enabled'))
        self._add_outputs()

    def _add_outputs(self) -> None:
        """Add outputs to the template for this resource."""
        self.template.add_output(Output(self.title,
                                        Value=self.ref()))
        self.template.add_output(Output(f'{self.title}Arn',
                                        Value=self.get_att('Arn')))

    def _get_bucket_name(self) -> str:
        """Return the name to use for the bucket."""
        provided = self._vars.get('BucketName')
        return provided if provided else \
            f'{self._stack_fqn.lower()}-{self._context.bucket_region}'

    def _get_encryption_settings(self) -> s3.BucketEncryption:
        """Get CFNgin Bucket encryption settings.

        Returns:
            S3 Bucket encryption settings.

        """
        kwargs = {'SSEAlgorithm': 'AES256'}
        kms_key_id = self._vars.get('KMSMasterKeyID')
        if kms_key_id:
            kwargs = {'KMSMasterKeyID': kms_key_id,
                      'SSEAlgorithm': 'aws:kms'}
        return s3.BucketEncryption(
            ServerSideEncryptionConfiguration=[s3.ServerSideEncryptionRule(
                ServerSideEncryptionByDefault=s3.ServerSideEncryptionByDefault(
                    **kwargs))])
