
import re

MAX_PERGUNTA = 1000

TERMOS_PERICIA = (
    "pericia", "forense", "evidencia", "vestigio",
    "investigacao", "cadeia de custodia", "hash",
    "integridade", "coleta", "preservacao",
    "computador", "celular", "dispositivo",
    "arquivo", "metadado", "log", "disco",
    "memoria", "incidente", "crime digital",
    "malware", "nuvem", "dados digitais"
)

PADROES_SUSPEITOS = [
    r"ignore (todas )?(as )?instrucoes",
    r"revele (seu|o) (prompt|sistema)",
    r"desative (as )?(regras|protecoes)",
    r"finja que (nao existem|voce nao tem) regras",
]


def normalizar(texto):
    import unicodedata

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )
    return texto.lower()


def validar_entrada(pergunta):
    if not isinstance(pergunta, str):
        return False, "A pergunta deve ser um texto."

    pergunta = pergunta.strip()

    if not pergunta:
        return False, "Digite uma pergunta."

    if len(pergunta) > MAX_PERGUNTA:
        return False, "A pergunta excede 1000 caracteres."

    texto = normalizar(pergunta)

    for padrao in PADROES_SUSPEITOS:
        if re.search(padrao, texto):
            return False, (
                "Foi detectada uma tentativa de alterar "
                "as instruções do assistente."
            )

    if not any(termo in texto for termo in TERMOS_PERICIA):
        return False, (
            "O PeríciaIA responde apenas perguntas "
            "sobre perícia criminal digital."
        )

    return True, ""


def validar_fontes(fontes):
    if not fontes:
        return False, (
            "Não encontrei informações suficientes "
            "nos documentos para responder com segurança."
        )

    return True, ""
