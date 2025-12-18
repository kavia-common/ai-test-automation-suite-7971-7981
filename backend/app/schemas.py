from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class TestCaseCreateSchema(Schema):
    """Schema for creating a test case."""
    title = fields.String(required=True, validate=validate.Length(min=1), description="Title of the test case")
    description = fields.String(required=False, missing="", description="Optional description")
    status = fields.String(required=False, missing="draft", validate=validate.OneOf(["draft", "active", "archived"]), description="Status of the test case")


# PUBLIC_INTERFACE
class TestCaseUpdateSchema(Schema):
    """Schema for updating a test case."""
    title = fields.String(required=False, validate=validate.Length(min=1), description="Title of the test case")
    description = fields.String(required=False, description="Optional description")
    status = fields.String(required=False, validate=validate.OneOf(["draft", "active", "archived"]), description="Status of the test case")


# PUBLIC_INTERFACE
class TestCaseSchema(Schema):
    """Schema for returning a test case."""
    id = fields.Int(required=True)
    title = fields.String(required=True)
    description = fields.String(allow_none=True)
    status = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# PUBLIC_INTERFACE
class ExecutionCreateSchema(Schema):
    """Schema for creating an execution for a test case."""
    test_case_id = fields.Int(required=True, description="ID of the test case to execute")


# PUBLIC_INTERFACE
class ExecutionSchema(Schema):
    """Schema for returning an execution."""
    id = fields.Int(required=True)
    test_case_id = fields.Int(required=True)
    status = fields.String(required=True, validate=validate.OneOf(["queued", "running", "passed", "failed"]))
    started_at = fields.DateTime(allow_none=True)
    finished_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# PUBLIC_INTERFACE
class ReportSchema(Schema):
    """Schema for returning a report."""
    id = fields.Int(required=True)
    execution_id = fields.Int(required=True)
    summary = fields.String(allow_none=True)
    details = fields.String(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# PUBLIC_INTERFACE
class ReportCreateSchema(Schema):
    """Schema for creating a report (mainly internal)."""
    execution_id = fields.Int(required=True)
    summary = fields.String(required=False, missing="")
    details = fields.String(required=False, missing="")


# PUBLIC_INTERFACE
class AITestGenRequestSchema(Schema):
    """Schema for AI test generation input."""
    prompt = fields.String(required=True, description="Natural language description of the test requirements")


# PUBLIC_INTERFACE
class AITestGenResponseSchema(Schema):
    """Schema for AI test generation response (stub)."""
    suggestions = fields.List(fields.Nested(TestCaseCreateSchema), required=True, description="Suggested test case drafts based on the prompt")
