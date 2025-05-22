# 🌶️ SpiceCode CLI - The next generation of code analysis 🔥🥵
### *"Aquele que controla o código, controla o futuro."*     
![small](https://github.com/user-attachments/assets/d659312e-d5cf-4442-98a9-004f59bb291b)

## Introdução

Bem-vindo ao SpiceCode CLI, a próxima geração de análise de código. Como os Fremen que dominam as areias de Arrakis, o SpiceCode permite que você navegue pelo deserto do desenvolvimento com precisão e sabedoria, extraindo insights valiosos do seu código.

SpiceCode é uma ferramenta de linha de comando desenvolvida para analisar e aprimorar seu código em várias linguagens de programação. Assim como a especiaria melange revela os segredos do universo, o SpiceCode revela os padrões, métricas e potenciais melhorias em sua base de código.

Nossa ferramenta foi construída com foco na simplicidade e eficiência, permitindo que desenvolvedores de todos os níveis - desde os jovens Fremen até os experientes Mentats - possam compreender e melhorar a qualidade de seus projetos.

### Características Principais

- **Análise Profunda**: Examina seu código e fornece métricas detalhadas
- **Suporte Multi-linguagem**: Compatível com Python, JavaScript, Ruby e Go
- **Lexers e Parsers Nativos**: Todos os analisadores são construídos por nós, sem dependências externas
- **Interface Amigável**: Comandos simples e intuitivos para facilitar o uso
- **Exportação de Resultados**: Exporte suas análises em diversos formatos (JSON, CSV, Markdown, HTML)
- **Suporte a Múltiplos Idiomas**: Interface traduzível para diferentes línguas

A água da vida é preciosa no deserto, assim como o código limpo é valioso em um projeto. Deixe o SpiceCode ser seu stillsuit, protegendo e otimizando seus recursos mais valiosos.

## Instalação

Para começar sua jornada com o SpiceCode, você precisará preparar seu ambiente como um verdadeiro Fremen prepara seu equipamento antes de atravessar o deserto.

### Pré-requisitos

- Python instalado em seu sistema (como a água, essencial para a vida)
- Terminal ou prompt de comando (seu thopter pessoal para navegar pelo código)

### Instalação via PIP

A maneira mais simples de obter o SpiceCode é através do PIP, o gerenciador de pacotes do Python:

```bash
pip install spicecode
```

Após a instalação, o comando `spice` estará disponível em seu terminal, como uma faca crysknife sempre ao seu alcance.

### Instalação a partir do Código-fonte

Se preferir construir a partir do código-fonte (como os Fremen que fabricam seus próprios equipamentos):

1. Clone o repositório para sua máquina:
   ```bash
   git clone https://github.com/spicecodecli/spicecode.git
   ```

2. Navegue até a pasta do projeto clonado:
   ```bash
   cd spicecode
   ```

3. Crie um ambiente virtual Python (venv):
   ```bash
   python -m venv venv
   ```

4. Ative seu ambiente virtual:
   
   **Windows**:
   ```bash
   ./venv/Scripts/activate
   ```
   
   **Linux/macOS**:
   ```bash
   source ./venv/bin/activate
   ```

5. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

6. Instale (build) o pacote SpiceCode localmente:
   ```bash
   pip install -e .
   ```

Agora você está pronto para começar sua jornada pelo deserto do código, com todas as ferramentas necessárias ao seu dispor.

### Verificando a Instalação

Para confirmar que o SpiceCode foi instalado corretamente, execute:

```bash
spice version
```

Se tudo estiver funcionando corretamente, você verá a versão atual do SpiceCode, confirmando que a especiaria flui em seu sistema.

## Uso

Como um Fremen que domina as técnicas de sobrevivência no deserto, você agora pode utilizar o SpiceCode para navegar pelo vasto oceano de areia que é seu código. Aqui estão os comandos principais que você pode executar:

### Comandos Básicos

#### Verificar a Versão
```bash
spice version
```
Este comando mostra a versão atual do SpiceCode instalada em seu sistema.

#### Mensagem de Boas-vindas
```bash
spice hello
```
Uma simples mensagem de boas-vindas, como o ritual de saudação entre os Fremen.

#### Configurar Idioma
```bash
spice translate
```
Configure o idioma da interface do SpiceCode. Como os dialetos de Arrakis, você pode escolher o que melhor se adapta às suas necessidades.

### Análise de Código

O coração do SpiceCode está em sua capacidade de analisar código, como um Mentat processando informações complexas:

#### Análise Básica
```bash
spice analyze ARQUIVO
```
Substitua `ARQUIVO` pelo caminho do arquivo que deseja analisar. Por exemplo:
```bash
spice analyze codigo.js
```

Este comando analisará o arquivo especificado e apresentará um menu interativo com diferentes opções de análise.

#### Análise Completa
```bash
spice analyze ARQUIVO --all
```
Executa todas as análises disponíveis para o arquivo sem exibir o menu de seleção.

#### Saída em JSON
```bash
spice analyze ARQUIVO --json
```
Retorna os resultados da análise em formato JSON, ideal para integração com outras ferramentas.

### Exportação de Resultados

Como os Fremen que preservam cada gota de água, você pode salvar os resultados de suas análises em diferentes formatos:

```bash
spice export ARQUIVO --format FORMATO --output CAMINHO_SAIDA
```

Onde:
- `ARQUIVO` é o caminho do arquivo a ser analisado
- `FORMATO` pode ser json, csv, markdown ou html
- `CAMINHO_SAIDA` é o caminho onde o arquivo de resultados será salvo

Exemplo:
```bash
spice export codigo.js --format markdown --output resultados.md
```

### Linguagens Suportadas

O SpiceCode, como um navegador experiente que conhece diferentes terrenos, suporta análise para as seguintes linguagens:

[![My Skills](https://skillicons.dev/icons?i=python,js,ruby,go&perline=10)](https://skillicons.dev)

- Python (`.py`)
- JavaScript (`.js`)
- Ruby (`.rb`)
- Go (`.go`)

Cada linguagem tem seu próprio lexer e parser nativos, construídos especificamente para o SpiceCode, sem dependências de bibliotecas externas - assim como os Fremen que constroem suas próprias ferramentas a partir dos recursos disponíveis em Arrakis.

## Contribuição

Como os Fremen que compartilham seu conhecimento para o bem da tribo, você também pode contribuir para o SpiceCode. No entanto, como este é atualmente um projeto acadêmico, há algumas considerações especiais:

### Status Atual do Projeto

Atualmente, o SpiceCode é um trabalho acadêmico e, por isso, não está aceitando contribuições externas. Como a água que é guardada nos reservatórios secretos dos Fremen, o desenvolvimento está temporariamente restrito à equipe original.

No entanto, planejamos abrir o projeto para contribuições da comunidade no futuro, quando nossa jornada acadêmica estiver completa. Sua paciência é valorizada como a virtude mais importante no deserto.

### Reportando Problemas

Mesmo que contribuições diretas de código não sejam aceitas no momento, você pode ajudar reportando problemas ou sugestões:

1. Acesse a [página de issues](https://github.com/spicecodecli/spicecode/issues) no GitHub
2. Clique em "New Issue"
3. Descreva o problema ou sugestão com o máximo de detalhes possível
4. Adicione labels relevantes como "bug" ou "enhancement"

### Código de Conduta

Como os Fremen que seguem regras estritas para sobreviver no deserto, todos os participantes do projeto SpiceCode devem aderir ao nosso Código de Conduta. Este código é inspirado no Contributor Covenant e adaptado com a temática de Dune.

Os principais pontos incluem:

- Mostrar gentileza, paciência e respeito aos companheiros de jornada
- Honrar diferenças em estilos de código, ideias e perspectivas
- Fornecer feedback construtivo com humildade e recebê-lo com graça
- Aceitar responsabilidade por erros e se esforçar para melhorar
- Trabalhar pelo bem maior da comunidade, não apenas pelo ganho pessoal

Para mais detalhes, consulte o arquivo [CODE_OF_CONDUCT.md](https://github.com/spicecodecli/spicecode/blob/main/CODE_OF_CONDUCT.md) no repositório.

### Futuras Contribuições

Quando o projeto for aberto para contribuições, seguiremos o modelo tradicional de fork e pull request:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Envie para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

Aguardamos ansiosamente o dia em que a comunidade poderá contribuir diretamente para o SpiceCode, como os Fremen que compartilham seu conhecimento para o benefício de todos em Arrakis.

## Segurança

Como os Fremen que protegem seus sietchs com vigilância constante, a segurança é uma prioridade no SpiceCode.

### Política de Segurança

O SpiceCode segue uma política de segurança simples mas eficaz:

| Versão | Suportada |
| ------ | --------- |
| Mais recente | ✅ |
| Não mais recente | ❌ |

Assim como os Fremen que mantêm seus equipamentos sempre atualizados para sobreviver no deserto, recomendamos que você sempre utilize a versão mais recente do SpiceCode para garantir a melhor experiência e segurança.

### Reportando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança no SpiceCode, por favor, reporte-a imediatamente:

1. Acesse a [página de issues](https://github.com/spicecodecli/spicecode/issues) no GitHub
2. Crie uma nova issue com os labels "bug" ou "security"
3. Descreva a vulnerabilidade com o máximo de detalhes possível
4. Se possível, inclua passos para reproduzir o problema

Nossa equipe, como os vigilantes Fremen que protegem as reservas de água, tratará todas as vulnerabilidades reportadas com a máxima prioridade e discrição.

### Práticas Recomendadas

Para garantir a segurança ao utilizar o SpiceCode:

- Sempre verifique a origem do código que está sendo analisado
- Mantenha o SpiceCode atualizado com a versão mais recente
- Utilize ambientes virtuais Python para isolar suas dependências
- Revise os resultados das análises antes de aplicar quaisquer mudanças sugeridas

Lembre-se: a vigilância constante é o preço da segurança, assim como os Fremen nunca baixam a guarda no deserto hostil de Arrakis.

## Licença

O SpiceCode é distribuído sob a licença Apache 2.0, uma licença permissiva que, como as leis dos Fremen, estabelece regras claras para o benefício de todos.

### Apache License 2.0

A licença Apache 2.0 permite:

- **Uso Comercial** ✅ - Como as caravanas de especiarias que cruzam o deserto, você pode usar o SpiceCode em projetos comerciais
- **Modificação** ✅ - Assim como os Fremen adaptam seus equipamentos, você pode modificar o código
- **Distribuição** ✅ - Compartilhe o conhecimento como os Fremen compartilham a água
- **Uso de Patente** ✅ - As patentes dos contribuidores são licenciadas para uso
- **Uso Privado** ✅ - Use o SpiceCode em seus projetos privados, como os segredos guardados nas cavernas

A licença Apache 2.0 não permite:

- **Uso de Marca Registrada** ❌ - O nome e logotipo do SpiceCode são protegidos
- **Responsabilidade** ❌ - Os criadores não são responsáveis por danos causados pelo uso do software
- **Garantia** ❌ - O software é fornecido "como está", sem garantias

### Requisitos da Licença

Ao utilizar, modificar ou distribuir o SpiceCode, você deve:

1. Incluir uma cópia da licença em qualquer redistribuição
2. Indicar claramente quaisquer mudanças feitas nos arquivos
3. Manter os avisos de direitos autorais e atribuições

Para mais detalhes, consulte o arquivo [LICENSE](https://github.com/spicecodecli/spicecode/blob/main/LICENSE) no repositório.

Como dizem os Fremen: "Respeite as regras do deserto, e o deserto respeitará você."

## FAQ e Solução de Problemas

Como um Fremen que enfrenta os desafios do deserto com sabedoria, aqui estão respostas para perguntas frequentes e soluções para problemas comuns que você pode encontrar ao utilizar o SpiceCode.

### Perguntas Frequentes

#### O que torna o SpiceCode diferente de outras ferramentas de análise de código?

O SpiceCode foi desenvolvido com foco na simplicidade e independência. Todos os lexers e parsers são construídos nativamente, sem depender de bibliotecas externas de análise de código. Isso nos dá controle total sobre o processo de análise e permite uma experiência mais consistente entre as diferentes linguagens suportadas.

#### Quais métricas o SpiceCode analisa?

O SpiceCode analisa diversas métricas, incluindo:
- Proporção de comentários no código
- Complexidade de funções e métodos
- Padrões de nomenclatura
- Estrutura do código
- Contagem de tipos de métodos

Novas métricas são adicionadas regularmente, como novas descobertas no deserto de Arrakis.

#### O SpiceCode funciona em todos os sistemas operacionais?

Sim! Como os Fremen que se adaptam a diferentes regiões do deserto, o SpiceCode funciona em Windows, macOS e Linux, desde que você tenha Python instalado.

#### Posso usar o SpiceCode em projetos comerciais?

Absolutamente! O SpiceCode é distribuído sob a licença Apache 2.0, que permite uso comercial. Consulte a seção de Licença para mais detalhes.

### Solução de Problemas

#### O comando `spice` não é reconhecido após a instalação

**Problema**: Após instalar o SpiceCode, o terminal não reconhece o comando `spice`.

**Solução**: 
1. Verifique se o Python está no PATH do seu sistema
2. Tente reinstalar o pacote com `pip install --user spicecode`
3. Em alguns sistemas, pode ser necessário usar `python -m spicecode` em vez de `spice`

#### Erro ao analisar arquivos grandes

**Problema**: O SpiceCode apresenta erros ou lentidão ao analisar arquivos muito grandes.

**Solução**:
1. Considere dividir o arquivo em partes menores
2. Verifique se seu sistema tem memória suficiente disponível
3. Atualize para a versão mais recente do SpiceCode, que pode conter otimizações

#### Problemas com caracteres especiais em nomes de arquivos

**Problema**: Erros ao analisar arquivos com caracteres especiais ou espaços no nome.

**Solução**:
1. Use aspas ao redor do nome do arquivo: `spice analyze "meu arquivo.js"`
2. Evite caracteres especiais em nomes de arquivos quando possível
3. Use a notação de escape apropriada para seu sistema operacional

#### A análise não reconhece corretamente minha linguagem de programação

**Problema**: O SpiceCode não identifica corretamente a linguagem do arquivo que está sendo analisado.

**Solução**:
1. Verifique se a extensão do arquivo está correta (.py, .js, .rb, .go)
2. Certifique-se de que está usando a versão mais recente do SpiceCode
3. Se o problema persistir, reporte-o como uma issue no GitHub

Como dizem os Fremen: "O homem que pode destruir uma coisa, controla essa coisa." Conhecer os problemas e suas soluções dá a você controle sobre sua experiência com o SpiceCode.

---

**Visite nossa página no registro PyPI**: [https://pypi.org/project/spicecode/](https://pypi.org/project/spicecode/)

*A especiaria deve fluir, e seu código deve ser apimentado!* 🌶️🔥
