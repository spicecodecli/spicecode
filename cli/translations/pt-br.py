messages = {
    # chaves para o comando hello
    "welcome": "🌶️   Bem-vindo ao [bold red]SpiceCode[/]! 🌶️",
    "description": "🔥 A ferramenta [yellow]CLI[/] que deixa seu código [yellow]mais spicy[/] 🥵",
    # mensagens de erro
    "error": "Erro:",
    "error_file_not_found": "Erro: Arquivo não encontrado",
    "error_not_a_file": "Erro: Não é um arquivo",
    "error_reading_file": "Erro ao ler o arquivo",
    "error_invalid_format": "Erro: Formato de saída inválido",
    "error_unexpected_result": "Erro: Resultado inesperado do analisador.",
    "error_analyzing_visibility": "Erro ao analisar visibilidade",
    # chaves para a saída do comando analyze
    "analyzing_file": "Analisando arquivo",
    "line_count": "O arquivo tem {count} linhas",
    "function_count": "O arquivo tem {count} funções",
    "comment_line_count": "O arquivo tem {count} linhas de comentário",
    "inline_comment_count": "O arquivo tem {count} comentários inline",
    # chaves para o menu de seleção do comando analyze
    "select_stats": "Selecione as estatísticas para exibir:",
    "line_count_option": "Contagem de Linhas",
    "function_count_option": "Contagem de Funções", 
    "comment_line_count_option": "Contagem de Linhas de Comentário",
    "inline_comment_count_option": "Contagem de Comentários Inline",
    "no_stats_selected": "Nenhuma estatística selecionada. Análise cancelada.",
    "confirm_and_analyze": "Confirmar e analisar",
    "checkbox_hint": "(Use espaço para selecionar, enter para confirmar)",
    # chaves para o comando version
    "version_info": "Versão do SpiceCode:",
    "version_not_found": "Informação de versão não encontrada no setup.py",
    "setup_not_found": "Erro: setup.py não encontrado.",

    # Geral / Reutilizável
    "file_path_help": "O caminho para o arquivo a ser analisado.",
    "output_format_help": "Formato de saída (console, json).",
    "valid_formats_are": "Formatos válidos são",
    "line_num": "Nº Linha",
    "content_col": "Conteúdo",
    "empty_line": "Vazia/Espaço em branco", # para exibir na célula da tabela
    "summary_statistics": "Estatísticas Resumidas",
    "metric": "Métrica",
    "value": "Valor",
    "category": "Categoria",
    "count": "Contagem",
    "name": "Nome",
    "type": "Tipo", # para tipo de função/método
    "visibility": "Visibilidade",

    # Análise de Indentação
    "analyze_indentation_help": "Analisa e reporta os níveis de indentação para cada linha no arquivo fornecido.",
    "indentation_analysis_for": "Análise de Indentação para",
    "indentation_details_per_line": "Detalhes de Indentação por Linha",
    "indent_level_col": "Nível de Indentação",

    # Análise de Dependências
    "analyze_dependencies_help": "Analisa e reporta as dependências externas para o arquivo fornecido.",
    "dependency_analysis_for": "Análise de Dependências para",
    "dependencies_found": "Dependências Encontradas",
    "dependency_name": "Nome da Dependência",
    "no_dependencies_found": "Nenhuma dependência encontrada neste arquivo.",

    # Análise de Proporção Comentário/Código
    "analyze_comment_code_ratio_help": "Analisa e reporta a proporção de comentários para código no arquivo fornecido.",
    "comment_code_ratio_analysis_for": "Análise de Proporção Comentário/Código para",
    "total_lines": "Total de Linhas",
    "code_lines": "Linhas de Código",
    "comment_lines": "Linhas Apenas de Comentário",
    "empty_lines": "Linhas Vazias/Espaços em Branco",
    "comment_code_ratio": "Proporção Comentário/Código",
    "line_by_line_classification": "Classificação Linha por Linha",
    "line_type": "Tipo de Linha",
    "code": "Código", # como tipo de linha
    "comment_only": "Apenas Comentário", # como tipo de linha
    "empty_or_whitespace": "Vazia/Espaço em branco", # como tipo de linha (chave para lógica)

    # Análise de Visibilidade
    "analyze_visibility_help": "Analisa e reporta a visibilidade de funções e métodos (público/privado) no arquivo fornecido.",
    "visibility_analysis_for": "Análise de Visibilidade para",
    "visibility_summary": "Resumo de Visibilidade",
    "public_functions": "Funções Públicas",
    "private_functions": "Funções Privadas",
    "public_methods": "Métodos Públicos",
    "private_methods": "Métodos Privados",
    "details_by_element": "Detalhes por Elemento",
    "function": "Função", # como tipo de elemento
    "method": "Método", # como tipo de elemento
    "public": "Público", # como status de visibilidade
    "private (convention)": "Privado (convenção)",
    "private (name mangling)": "Privado (name mangling)",
    "no_elements_found_for_visibility": "Nenhuma função ou método encontrado para análise de visibilidade neste arquivo."
}

