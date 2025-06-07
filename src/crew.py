import os
import yaml
import pandas as pd
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Carregar variáveis de ambiente
load_dotenv()

class FiscalCrew:
    def __init__(self):
        self.llm = Ollama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        self.df_cabecalho = None
        self.df_itens = None
        self._load_data()
        
    def _load_data(self):
        """Carrega os dados dos arquivos CSV"""
        try:
            cabecalho_path = os.getenv("CSV_CABECALHO_PATH")
            itens_path = os.getenv("CSV_ITENS_PATH")
            
            if cabecalho_path and os.path.exists(cabecalho_path):
                self.df_cabecalho = pd.read_csv(cabecalho_path)
                print(f"✅ Arquivo cabeçalho carregado: {len(self.df_cabecalho)} registros")
            
            if itens_path and os.path.exists(itens_path):
                self.df_itens = pd.read_csv(itens_path)
                print(f"✅ Arquivo itens carregado: {len(self.df_itens)} registros")
                
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {str(e)}")
    
    def _get_data_summary(self):
        """Retorna resumo dos dados para o agente"""
        summary = "DADOS DISPONÍVEIS:\n\n"
        
        if self.df_cabecalho is not None:
            summary += f"CABEÇALHO DAS NOTAS FISCAIS ({len(self.df_cabecalho)} registros):\n"
            summary += f"Colunas: {', '.join(self.df_cabecalho.columns.tolist())}\n"
            summary += f"Período: {self.df_cabecalho['DATA EMISSÃO'].min()} a {self.df_cabecalho['DATA EMISSÃO'].max()}\n\n"
        
        if self.df_itens is not None:
            summary += f"ITENS DAS NOTAS FISCAIS ({len(self.df_itens)} registros):\n"
            summary += f"Colunas: {', '.join(self.df_itens.columns.tolist())}\n\n"
            
        return summary
    
    def create_agent(self):
        """Cria o agente especialista fiscal"""
        data_summary = self._get_data_summary()
        
        return Agent(
            role="Especialista em Análise Fiscal",
            goal="Analisar dados de notas fiscais e fornecer respostas precisas sobre questões tributárias",
            backstory=f"""Você é um analista fiscal sênior com anos de experiência em regulamentações brasileiras.
            Você tem acesso aos seguintes dados:
            
            {data_summary}
            
            Use estes dados para responder perguntas sobre impostos, fornecedores, produtos e conformidade fiscal.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_task(self, pergunta):
        """Cria uma tarefa baseada na pergunta do usuário"""
        # Preparar contexto com dados relevantes
        contexto_dados = ""
        
        if self.df_cabecalho is not None:
            contexto_dados += f"\nDADOS DO CABEÇALHO:\n{self.df_cabecalho.head().to_string()}\n"
        
        if self.df_itens is not None:
            contexto_dados += f"\nDADOS DOS ITENS:\n{self.df_itens.head().to_string()}\n"
        
        return Task(
            description=f"""
            Analise a seguinte pergunta sobre dados fiscais: {pergunta}
            
            Contexto dos dados disponíveis:
            {contexto_dados}
            
            Instruções:
            1. Analise os dados relevantes para responder a pergunta
            2. Forneça números específicos e exemplos concretos
            3. Cite valores, códigos e referências quando aplicável
            4. Se não encontrar dados suficientes, informe claramente
            """,
            expected_output="""
            Uma resposta estruturada contendo:
            - Análise detalhada baseada nos dados
            - Valores específicos e estatísticas
            - Exemplos concretos dos dados
            - Recomendações quando aplicável
            """,
            agent=None  # Será definido no método run
        )
    
    def run(self, pergunta):
        """Executa a análise baseada na pergunta"""
        try:
            agent = self.create_agent()
            task = self.create_task(pergunta)
            task.agent = agent
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )
            
            resultado = crew.kickoff()
            return str(resultado)
            
        except Exception as e:
            return f"❌ Erro na análise: {str(e)}"
    
    def get_data_info(self):
        """Retorna informações sobre os dados carregados"""
        info = {}
        
        if self.df_cabecalho is not None:
            info['cabecalho'] = {
                'registros': len(self.df_cabecalho),
                'colunas': self.df_cabecalho.columns.tolist(),
                'periodo': f"{self.df_cabecalho['DATA EMISSÃO'].min()} a {self.df_cabecalho['DATA EMISSÃO'].max()}"
            }
        
        if self.df_itens is not None:
            info['itens'] = {
                'registros': len(self.df_itens),
                'colunas': self.df_itens.columns.tolist()
            }
            
        return info