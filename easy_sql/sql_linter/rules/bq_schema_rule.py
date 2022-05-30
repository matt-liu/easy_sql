"""An example of a custom rule implemented through the plugin system."""

from sqlfluff.core.rules.base import (
    BaseRule,
    LintResult,
    RuleContext,
)

class Rule_BigQuery_L001(BaseRule):
    """select from is compulsory to have schema
    **Anti-pattern**
    use select from table without schema
    .. code-block:: sql
        SELECT *
        FROM foo
    **Best practice**
    Do not order by these columns.
    .. code-block:: sql
        SELECT *
        FROM test.foo
    """

    groups = ("all", "bigquery")

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)
        self.force_schema = True

    def _eval(self, context: RuleContext):
        """check from table have schema"""
        if context.segment.is_type("table_reference") and self.force_schema:
            if len(context.segment.segments) != 3:
                return LintResult(
                    anchor=context.segment,
                    description=f"select from `{context.segment.raw}` do not have schema in table.",
                )
