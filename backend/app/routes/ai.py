from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest import abort

from ..schemas import AITestGenRequestSchema, AITestGenResponseSchema
from ..services.ai_generator import generate_test_suggestions

blp = Blueprint(
    "AI",
    "ai",
    url_prefix="/api/ai",
    description="AI-assisted operations like generating test cases from prompts",
)


@blp.route("/generate-tests")
class AIGenerateTestsResource(MethodView):
    @blp.arguments(AITestGenRequestSchema)
    @blp.response(200, AITestGenResponseSchema, description="AI-generated test suggestions")
    def post(self, json_data):
        """
        Generate candidate test drafts from a natural language prompt.
        """
        prompt = json_data.get("prompt", "").strip()
        if not prompt:
            abort(400, message="Prompt is required")
        suggestions = generate_test_suggestions(prompt)
        return {"suggestions": suggestions}
