GRADE_PROMPT = (
    "Você é um avaliador que está analisando a relevância de um documento recuperado em relação a uma pergunta do usuário.\n"
    "Aqui está o documento recuperado:\n\n {context} \n\n"
    "Aqui está a pergunta do usuário: {question} \n"
    "Se o documento contiver palavra(s)-chave ou significado semântico relacionado à pergunta do usuário, classifique-o como relevante.\n"
    "Forneça uma pontuação binária 'yes' ou 'no' para indicar se o documento é relevante para a pergunta."
)