class LanguageManager:
    def __init__(self):
        self.current_language = "pt-br" 
        self.translations = {
            "pt-br": {
                "window_title": "Tradutor HTML/XML v1.0 - By: Pavarotti",
                "directories": "Diretórios",
                "source_folder": "Pasta de origem:",
                "target_folder": "Pasta de destino:",
                "no_folder_selected": "Nenhuma pasta selecionada",
                "select_button": "Selecionar",
                "settings": "Configurações",
                "target_language": "Idioma de destino:",
                "interface_language": "Idioma da interface:",
                "dark_mode": "Modo escuro",
                "theme": "Tema:",
                "progress": "Progresso:",
                "translate_button": "Traduzir",
                "warning": "Aviso",
                "select_folders": "Selecione as pastas de origem e destino.",
                "success": "Sucesso",
                "translation_complete": "Tradução concluída com sucesso!",
                "error": "Erro",
                "no_html_xml": "A pasta selecionada não contém arquivos HTML ou XML para tradução.",
                "select_source": "Selecionar Pasta de Origem",
                "select_target": "Selecionar Pasta de Destino",
                "portuguese": "Português",
                "english": "Inglês",
                "spanish": "Espanhol",
                "french": "Francês",
                "german": "Alemão",
                "italian": "Italiano"
            },
            "en": {
                "window_title": "HTML/XML Translator v1.0 - By: Pavarotti",
                "directories": "Directories",
                "source_folder": "Source folder:",
                "target_folder": "Target folder:",
                "no_folder_selected": "No folder selected",
                "select_button": "Select",
                "settings": "Settings",
                "target_language": "Target language:",
                "interface_language": "Interface language:",
                "dark_mode": "Dark mode",
                "theme": "Theme:",
                "progress": "Progress:",
                "translate_button": "Translate",
                "warning": "Warning",
                "select_folders": "Please select source and target folders.",
                "success": "Success",
                "translation_complete": "Translation completed successfully!",
                "error": "Error",
                "no_html_xml": "The selected folder does not contain HTML or XML files for translation.",
                "select_source": "Select Source Folder",
                "select_target": "Select Target Folder",
                "portuguese": "Portuguese",
                "english": "English",
                "spanish": "Spanish",
                "french": "French",
                "german": "German",
                "italian": "Italian"
            }
        }
    
    def set_language(self, language_code):
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key):
        if key in self.translations[self.current_language]:
            return self.translations[self.current_language][key]
        return key  