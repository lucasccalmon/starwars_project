import mwxml
import mwparserfromhell
import csv
import re
import sys

# --- CONFIGURAÇÃO ---
DUMP_FILE = 'starwars_pages_current.xml' 
OUTPUT_CSV = 'personagens_star_wars_finalv2.csv'
BATCH_SIZE = 50 

# Lista de templates alvo
TARGET_TEMPLATES = {'Character', 'Infobox character', 'Infobox person', 'Droid', 'Infobox droid', 'Creature', 'Infobox creature'}

def limpar_texto(node):
    """
    Recebe um nó do mwparserfromhell e retorna texto limpo e achatado (sem quebras de linha).
    """
    if not node: return "N/A"
    
    # 1. Converte para string bruta primeiro para limpar tags XML/HTML pesadas
    texto_bruto = str(node)
    
    # Remove tags de referência inteiras <ref ...> ... </ref> ANTES de tirar o código wiki
    # Isso evita que fique sobrando números como [1], [2] no nome
    texto_bruto = re.sub(r'<ref.*?>.*?</ref>', '', texto_bruto, flags=re.IGNORECASE|re.DOTALL)
    texto_bruto = re.sub(r'<.*?>', '', texto_bruto) # Remove outras tags HTML (<br>, <div>)

    # 2. Usa o parser para limpar links ([[Link|Texto]] -> Texto) e formatação
    try:
        # Parseia de novo só esse pedaço para usar o strip_code
        cleaned = mwparserfromhell.parse(texto_bruto).strip_code()
    except:
        cleaned = texto_bruto

    # 3. Achatamento (Flattening) para CSV ficar em uma linha
    # Troca quebras de linha por ponto-e-vírgula
    cleaned = cleaned.replace('\n', '; ').replace('\r', '')
    
    # Remove asteriscos de lista (*) e limpa espaços extras
    cleaned = re.sub(r'\s*\*\s*', '', cleaned)
    cleaned = re.sub(r'\s+;', ';', cleaned) 
    cleaned = re.sub(r';+', ';', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Remove ponto e vírgula solto no inicio/fim
    if cleaned.startswith(';'): cleaned = cleaned[1:].strip()
    if cleaned.endswith(';'): cleaned = cleaned[:-1].strip()
    
    return cleaned if cleaned else "N/A"

def detectar_continuidade(titulo, texto_bruto, wikicode):
    """Define se é Canon ou Legends."""
    if titulo.endswith("/Legends"): return "Legends"
    if "Category:Legends articles" in texto_bruto: return "Legends"
    
    # Procura no template {{Top}} ou {{Eras}}
    templates_topo = wikicode.filter_templates(recursive=False)
    for t in templates_topo:
        nome = t.name.strip_code().strip().lower()
        if nome in ['top', 'eras', 'era icon']:
            for param in t.params:
                val = param.value.strip_code().strip().lower()
                if val == 'leg': return "Legends"
                
    return "Canon" # Default

def process_dump(dump, path):
    print(f"📖 Lendo arquivo: {path}")
    count = 0
    chars_found = 0
    
    # Colunas finais do CSV
    colunas = [
        'Nome', 'Continuidade', 'Tipo', 'Espécie', 'Gênero', 'Planeta Natal', 
        'Altura', 'Massa', 'Nascimento', 'Morte', 
        'Famílias', 'Pais', 'Parceiros', 'Irmãos', 'Filhos', 
        'Mestres', 'Aprendizes', 'Afiliação'
    ]
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(colunas)

        for page in dump:
            count += 1
            if count % 2000 == 0:
                print(f"   ...Lendo pág {count} (Personagens: {chars_found})", end='\r')

            if page.namespace != 0: continue

            for revision in page:
                if not revision.text: continue
                
                try:
                    # Parseia o texto
                    wikicode = mwparserfromhell.parse(revision.text)
                    
                    # Detecta continuidade
                    continuidade = detectar_continuidade(page.title, revision.text, wikicode)
                    
                    # Filtra templates
                    templates = wikicode.filter_templates()
                    is_character = False
                    
                    # Dicionário com valores padrão
                    row = {col: "N/A" for col in colunas}
                    row['Nome'] = page.title.replace("/Legends", "").strip()
                    row['Continuidade'] = continuidade

                    for template in templates:
                        name = template.name.strip_code().strip()
                        if name in TARGET_TEMPLATES:
                            is_character = True
                            
                            # Função auxiliar para pegar valor com segurança
                            def get_val(key):
                                if template.has(key):
                                    return limpar_texto(template.get(key).value)
                                return "N/A"

                            # Extração dos Campos Básicos
                            row['Tipo'] = get_val("type")
                            row['Espécie'] = get_val("species")
                            row['Gênero'] = get_val("gender")
                            row['Planeta Natal'] = get_val("homeworld")
                            row['Altura'] = get_val("height")
                            row['Massa'] = get_val("mass")
                            row['Nascimento'] = get_val("birth")
                            row['Morte'] = get_val("death")
                            row['Afiliação'] = get_val("affiliation")
                            # Extração dos Campos de Relacionamento (Novos)
                            row['Famílias'] = get_val("families")
                            row['Pais'] = get_val("parents")
                            row['Parceiros'] = get_val("partners")
                            row['Irmãos'] = get_val("siblings")
                            row['Filhos'] = get_val("children")
                            row['Mestres'] = get_val("masters")
                            row['Aprendizes'] = get_val("apprentices")
                            
                            if "Droid" in name or "droid" in name:
                                row['Espécie'] = get_val("class")
                                row['Tipo'] = get_val("model")
                                row['Pais'] = get_val("creator")

                            
                            break # Achou a infobox, para de procurar
                    
                    if is_character:
                        chars_found += 1
                        # Escreve a linha na ordem correta das colunas
                        writer.writerow([row[c] for c in colunas])
                        
                        if chars_found % BATCH_SIZE == 0:
                            f.flush()

                except Exception as e:
                    continue

    print(f"\n🏁 Finalizado! Total: {chars_found} personagens processados.")

if __name__ == "__main__":
    try:
        list(mwxml.map(process_dump, [DUMP_FILE]))
    except Exception as e:
        print(f"Erro Crítico: {e}")