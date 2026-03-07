CONTEXTUALIZE_PROMPT = (
    "Reescreva a última pergunta de forma autocontida usando o histórico abaixo. "
    "Se já for autocontida, retorne exatamente como está. NÃO responda, apenas reescreva.\n"
    "Histórico: {history}\n"
    "Última pergunta: {question}\n"
    "Pergunta reescrita:"
)