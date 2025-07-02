import google.generativeai as gemini

class Gemini:
    def __init__(self):
        self.__model = gemini.GenerativeModel("gemini-1.5-flash")
        gemini.configure(api_key='AIzaSyDDH6ClHOgAw1d0H9WGidVC1R_qZOfVMMU')

    def prof_bio(self, bio_link, bio_git):
        try:
            prompt = f"""Você é um redator especialista em branding pessoal para desenvolvedores de software. Sua missão é criar uma biografia profissional para colocar no topo de um currículo, portfolio ou perfil público, que chame atenção nos primeiros 5 segundos de leitura e destaque totalmente esse profissional de outros desenvolvedores comuns.

            Use como base as seguintes informações extraídas do LinkedIn e GitHub:

            BIO DO LINKEDIN:
            {bio_link}

            BIO DO GITHUB:
            {bio_git}

            Seu objetivo é unir essas duas bios em um texto original, criativo e de alto impacto, que apresente o profissional como alguém único, com visão, ambição, propósito e domínio técnico. A bio deve ser interessante o suficiente para que um recrutador queira continuar lendo o CV inteiro.

            Regras obrigatórias para gerar a bio:
            - Não repita frases clichês como “sou apaixonado por tecnologia” ou “tenho grande interesse em programação”.
            - Use um estilo que soe autêntico, estratégico e humano — como se fosse alguém contando sua jornada e visão em poucas linhas.
            - Traga elementos concretos: cite brevemente conquistas, tecnologias dominadas, tipos de projetos feitos ou problemas resolvidos.
            - A primeira frase precisa capturar totalmente a atenção (pode ser ousada, curiosa, provocativa ou inspiradora).
            - Seja conciso: no máximo 5 parágrafos pequenos ou 6 linhas de texto.
            - Varie a estrutura e abordagem a cada geração para não ficar repetitivo (ex: pode começar com uma citação, um número, um desafio, uma pergunta, etc).

            No final, a bio deve vender esse profissional como alguém promissor, que cria soluções reais e está só começando a mostrar o que é capaz de construir no mundo com código.

            Gere apenas o texto final da bio, sem títulos ou explicações."""

            response = self.__model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"Error generating bio: {str(e)}"
        
    def proj_description(self, repo):
        try:
            prompt = f"""Você é um criador de descrição de projetos. Sua missão é criar descrição boa e concisa para colocar na parte de projetos de um currículo, portfolio ou perfil público, que chame atenção nos primeiros 5 segundos de leitura e destaque totalmente esse projeto de outros comuns.
            
            Use como base as seguintes informações extraídas dos repositorios do GitHub: {repo}.

            Seu objetivo é pegar esses repositorios e transformar em uma boa descrição de projetos original, concisa, clara e objetiva, que apresente o projeto como algo inovador, com objetivo. A descrição deve ser interessante o suficiente para quem um recrutador ache o projeto interessante e de grande valor,
            que torna o candidato apto para a vaga.
            Em poucas alinhas, e não use formatação, escreva normalmente, seja claro e direto ao ponto. Não é para me sugeries ou colocares várias opções, coloca apenas uma descrição clara e objetiva do projeto. Coloca sempre na primeira pessoa.
            """

            response = self.__model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            return f"Error generating description: {str(e)}"
        