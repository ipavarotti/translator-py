import os
import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import xml.etree.ElementTree as ET


class HTMLXMLTranslator:
    def __init__(self):

        self.language_map = {
            "pt-br": "pt",  # Portuguese
            "en": "en",     # English
            "es": "es",     # Spanish
            "fr": "fr",     # French
            "de": "de",     # German
            "it": "it"      # Italian
        }
        
    def count_files(self, directory):
        """Conta o número de arquivos HTML e XML no diretório e subdiretórios."""
        count = 0
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.html', '.htm', '.xml')):
                    count += 1
        return count
    
    def translate_directory(self, source_dir, target_dir, target_language="pt-br", progress_callback=None):
        """Traduz todos os arquivos HTML e XML de um diretório para outro."""
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        if target_language in self.language_map:
            googletrans_lang = self.language_map[target_language]
        else:
            googletrans_lang = target_language
            
        for root, dirs, files in os.walk(source_dir):
            rel_path = os.path.relpath(root, source_dir)
            target_root = os.path.join(target_dir, rel_path) if rel_path != '.' else target_dir
            
            if not os.path.exists(target_root):
                os.makedirs(target_root)
            
            for file in files:
                if file.lower().endswith(('.html', '.htm')):
                    self._translate_html_file(
                        os.path.join(root, file),
                        os.path.join(target_root, file),
                        target_language
                    )
                    if progress_callback:
                        progress_callback()
                        
                elif file.lower().endswith('.xml'):
                    self._translate_xml_file(
                        os.path.join(root, file),
                        os.path.join(target_root, file),
                        target_language
                    )
                    if progress_callback:
                        progress_callback()
                else:
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_root, file)
                    with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                        dst.write(src.read())
    
    def _translate_html_file(self, source_file, target_file, target_language):
        """Traduz um arquivo HTML."""
        try:
            with open(source_file, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            if target_language in self.language_map:
                dest_lang = self.language_map[target_language]
            else:
                dest_lang = target_language
                
            translator = GoogleTranslator(source='auto', target=dest_lang)
            
            for element in soup.find_all(text=True):
                if element.parent.name not in ['script', 'style', 'meta', 'link']:
                    text = element.strip()
                    if text and not re.match(r'^[\s\d\W]+$', text) and len(text) > 1:
                        try:
                            import time
                            time.sleep(0.1)
                            
                            translated = translator.translate(text)
                            if translated:
                                new_string = soup.new_string(translated)
                                element.replace_with(new_string)
                        except Exception as e:
                            print(f"Erro ao traduzir texto: {text} - {str(e)}")
            
            for tag in soup.find_all(['img', 'input', 'button', 'a', 'meta']):
                if tag.has_attr('title') and tag['title'].strip():
                    try:
                        tag['title'] = translator.translate(tag['title'])
                    except:
                        pass
                        
                if tag.has_attr('alt') and tag['alt'].strip():
                    try:
                        tag['alt'] = translator.translate(tag['alt'])
                    except:
                        pass
                        
                if tag.has_attr('placeholder') and tag['placeholder'].strip():
                    try:
                        tag['placeholder'] = translator.translate(tag['placeholder'])
                    except:
                        pass
                        
                if tag.name == 'meta' and tag.has_attr('content') and tag.has_attr('name'):
                    if tag['name'] in ['description', 'keywords'] and tag['content'].strip():
                        try:
                            tag['content'] = translator.translate(tag['content'])
                        except:
                            pass
            
            with open(target_file, 'w', encoding='utf-8') as file:
                file.write(str(soup))
                
        except Exception as e:
            print(f"Erro ao traduzir {source_file}: {str(e)}")
            with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                dst.write(src.read())
    
    def _translate_xml_file(self, source_file, target_file, target_language):
        """Traduz um arquivo XML."""
        try:
            tree = ET.parse(source_file)
            root = tree.getroot()
            
            if target_language in self.language_map:
                dest_lang = self.language_map[target_language]
            else:
                dest_lang = target_language
            
            def translate_element(element):
                if element.text and element.text.strip():
                    text = element.text.strip()
                    if not re.match(r'^[\s\d\W]+$', text) and len(text) > 1:
                        try:
                            import time
                            time.sleep(0.1)
                            
                            translator = GoogleTranslator(source='auto', target=dest_lang)
                            translated = translator.translate(text)
                            if translated:
                                element.text = translated
                        except Exception as e:
                            print(f"Erro ao traduzir texto XML: {text} - {str(e)}")
                
                for attr_name, attr_value in element.attrib.items():
                    if attr_value.strip() and not re.match(r'^[\s\d\W]+$', attr_value) and len(attr_value) > 1:
                        try:
                            translator = GoogleTranslator(source='auto', target=dest_lang)
                            translated = translator.translate(attr_value)
                            if translated:
                                element.attrib[attr_name] = translated
                        except:
                            pass
                
                for child in element:
                    translate_element(child)
            
            translate_element(root)
            
            tree.write(target_file, encoding='utf-8', xml_declaration=True)
            
        except Exception as e:
            print(f"Erro ao traduzir {source_file}: {str(e)}")
            with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                dst.write(src.read())