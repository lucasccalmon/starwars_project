import mwxml
import mwparserfromhell

# --- CONFIGURAÇÃO ---
DUMP_FILE = 'starwars_pages_current.xml' 

# Lista exata de Títulos (baseada nos seus links)
# Note: Troquei "_" por " " pois é assim que está no banco de dados.
ALVOS_EXATOS = {
    "Nix"
}

def inspect_exact_pages(dump, path):
    print(f"🔎 Buscando APENAS pelos títulos: {ALVOS_EXATOS}...")
    
    encontrados = 0
    
    for page in dump:
        # 1. FILTRO DE NAMESPACE: Garante que é um artigo, não fórum/discussão
        # (Namespace 0 = Artigo Principal)
        if page.namespace != 0:
            continue

        # 2. BUSCA EXATA: O título tem que ser IDÊNTICO, letra por letra
        if page.title in ALVOS_EXATOS:
            print(f"\n{'='*60}")
            print(f"🎯 ALVO LOCALIZADO: {page.title}")
            print(f"{'='*60}")
            
            for revision in page:
                if not revision.text:
                    continue
                    
                # Parseia para achar a Infobox bonitinha
                wikicode = mwparserfromhell.parse(revision.text)
                templates = wikicode.filter_templates()
                
                # Dentro do loop da revision...
                wikicode = mwparserfromhell.parse(revision.text)

                print(wikicode)
                                        
                # Procura o template principal
                for template in templates:
                    
                    # O nome geralmente é 'Character', 'Infobox character' ou 'Infobox person'
                    nome_template = template.name.strip_code().strip()
                    if "Canon" in nome_template or "Legends" in nome_template or "Category" in nome_template:
                        print(nome_template)
                    if "Character" in nome_template or "Infobox" in nome_template:
                        print(f"📌 TEMPLATE USADO: {nome_template}")
                        print("-" * 30)
                        print("CAMPOS ENCONTRADOS (Copie estes nomes para seu script):")
                        
                        # Lista todos os parâmetros que essa página usa
                        for param in template.params:
                            chave = param.name.strip_code().strip()
                            valor = param.value.strip_code().strip()
                            # Mostra só os primeiros 50 caracteres do valor para não poluir
                            print(f"   • {chave} = {valor}")
                        
                        print("-" * 30)
                        break # Achou a infobox principal, para de listar templates desta página
            
            encontrados += 1
            if encontrados >= len(ALVOS_EXATOS):
                print("\n✅ Todos os alvos foram encontrados!")
                raise StopIteration

try:
    list(mwxml.map(inspect_exact_pages, [DUMP_FILE]))
except StopIteration:
    pass
except Exception as e:
    print(f"Erro: {e}")