"""Creates an S3 Bucket for CFNgin."""
from typing import Any, Dict

from runway.cfngin.blueprints.base import Blueprint
from troposphere import Template, AWSObject

from .resources.s3 import CFNginBucket

TEMPLATE_DESCRIPTION = 'Runway CFNgin Bucket'


class BlueprintClass(Blueprint):
    """Extends CFNgin's Blueprint class."""

    VARIABLES: Dict[str, Any] = CFNginBucket.VARIABLES

    @property
    def fqn(self) -> str:
        """Fully qualified name of the stack that will be produced."""
        return self.context.get_fqn(self.name)

    def add_resource(self, obj: AWSObject) -> None:
        """Add a resource object to the Blueprint.

        Args:
            obj: Subclass of a Troposphere resource that provisions
                itself during initialization.
        """
        obj(context=self.context,
            stack_fqn=self.fqn,
            template=self.template,
            variables=self.get_variables())

    def create_template(self) -> None:
        """Create template (method called by CFNgin)."""
        template: Template = self.template
        template.set_description(TEMPLATE_DESCRIPTION)
        template.set_version('2010-09-09')

        self.add_resource(CFNginBucket)
