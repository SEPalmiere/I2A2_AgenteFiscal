import streamlit as st
import os
from crew import FiscalCrew

# Configuração da página
st.set_page_config(
    page_title="Agente Fiscal - Análise de Notas Fiscais",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("🧾 Agente Fiscal - Análise de Notas Fiscais")
    st.markdown("---")
    
    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Informações do Sistema")
        
        # Verificar status do Ollama
        try:
            crew = FiscalCrew()
            data_info = crew.get_data_info()
            
            st.success("✅ Sistema Conectado")
            st.write(f"**Modelo:** {os.getenv('OLLAMA_MODEL', 'llama3.2:3b')}")
            
            if 'cabecalho' in data_info:
                st.write(f"**Cabeçalhos:** {data_info['cabecalho']['registros']} registros")
            
            if 'itens' in data_info:
                st.write(f"**Itens:** {data_info['itens']['registros']} registros")
                
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            st.stop()
    
    # Interface principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Faça sua pergunta sobre as Notas Fiscais")
        
        # Exemplos de perguntas
        with st.expander("📝 Exemplos de Perguntas"):
            st.write("""
            - Qual o valor total das notas fiscais?
            - Quais são os principais fornecedores?
            - Quantas notas foram emitidas em janeiro de 2024?
            - Qual o produto mais vendido?
            - Há alguma inconsistência nos dados?
            - Qual o valor médio por nota fiscal?
            """)
        
        # Campo de entrada da pergunta
        pergunta = st.text_area(
            "Digite sua pergunta:",
            height=100,
            placeholder="Ex: Qual o valor total das notas fiscais do mês de janeiro?"
        )
        
        # Botão para processar
        if st.button("🔍 Analisar", type="primary"):
            if pergunta.strip():
                with st.spinner("🤖 Analisando dados..."):
                    try:
                        crew = FiscalCrew()
                        resposta = crew.run(pergunta)
                        
                        st.success("✅ Análise concluída!")
                        st.markdown("### 📋 Resultado da Análise:")
                        st.markdown(resposta)
                        
                    except Exception as e:
                        st.error(f"❌ Erro na análise: {str(e)}")
            else:
                st.warning("⚠️ Por favor, digite uma pergunta.")
    
    with col2:
        st.header("📊 Status dos Dados")
        
        try:
            crew = FiscalCrew()
            data_info = crew.get_data_info()
            
            if 'cabecalho' in data_info:
                st.metric(
                    "Notas Fiscais (Cabeçalho)",
                    data_info['cabecalho']['registros']
                )
                
                with st.expander("Colunas Cabeçalho"):
                    for col in data_info['cabecalho']['colunas']:
                        st.write(f"• {col}")
            
            if 'itens' in data_info:
                st.metric(
                    "Itens das Notas",
                    data_info['itens']['registros']
                )
                
                with st.expander("Colunas Itens"):
                    for col in data_info['itens']['colunas']:
                        st.write(f"• {col}")
                        
        except Exception as e:
            st.error(f"Erro ao carregar informações: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            🤖 Agente Fiscal - Powered by CrewAI & Ollama
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()