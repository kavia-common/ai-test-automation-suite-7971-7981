from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..repository import (
    create_test_case,
    get_test_case,
    list_test_cases,
    update_test_case,
    delete_test_case,
)
from ..schemas import (
    TestCaseCreateSchema,
    TestCaseSchema,
    TestCaseUpdateSchema,
)

blp = Blueprint(
    "Tests",
    "tests",
    url_prefix="/api/tests",
    description="CRUD operations for test cases",
)


@blp.route("/")
class TestsListResource(MethodView):
    @blp.response(200, TestCaseSchema(many=True), description="List all tests")
    def get(self):
        """List all test cases."""
        return list_test_cases()

    @blp.arguments(TestCaseCreateSchema)
    @blp.response(201, TestCaseSchema, description="Create a new test case")
    def post(self, json_data):
        """Create a new test case."""
        obj = create_test_case(**json_data)
        return obj


@blp.route("/<int:test_id>")
class TestDetailResource(MethodView):
    @blp.response(200, TestCaseSchema, description="Get a test case by id")
    def get(self, test_id: int):
        """Get a test case by id."""
        obj = get_test_case(test_id)
        if not obj:
            abort(404, message="Test case not found")
        return obj

    @blp.arguments(TestCaseUpdateSchema)
    @blp.response(200, TestCaseSchema, description="Update a test case by id")
    def patch(self, json_data, test_id: int):
        """Update a test case by id."""
        obj = update_test_case(test_id, **json_data)
        if not obj:
            abort(404, message="Test case not found")
        return obj

    @blp.response(204, description="Delete a test case by id")
    def delete(self, test_id: int):
        """Delete a test case by id."""
        ok = delete_test_case(test_id)
        if not ok:
            abort(404, message="Test case not found")
        return ""
