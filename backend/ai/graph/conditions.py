from typing import Literal
from ai.models.models import gemini_25_flash
from ai.prompts.grade import GRADE_PROMPT
from ai.schemas.grading import GradeDocuments

def grade_documents(state) -> Literal["generate_answer", "rewrite_question"]:
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = gemini_25_flash.with_structured_output(GradeDocuments).invoke(
        [{"role": "user", "content": prompt}]
    )

    return (
        "generate_answer"
        if response.binary_grade == "yes"
        else "rewrite_question"
    )