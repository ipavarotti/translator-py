import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QComboBox,
                            QProgressBar, QMessageBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from translator.translator import HTMLXMLTranslator
from ui.theme_manager import ThemeManager
from ui.language_manager import LanguageManager
import sys  
import traceback  #

class TranslationThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, source_dir, target_dir, target_language):
        super().__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.target_language = target_language
        
    def run(self):
        try:
            translator = HTMLXMLTranslator()
            total_files = translator.count_files(self.source_dir)
            processed = 0
            
            def progress_callback():
                nonlocal processed
                processed += 1
                progress = int((processed / total_files) * 100)
                self.progress_signal.emit(progress)
            
            translator.translate_directory(
                self.source_dir, 
                self.target_dir, 
                self.target_language,
                progress_callback
            )
            self.finished_signal.emit(True, "Tradução concluída com sucesso!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro durante a tradução: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.source_dir = ""
        self.target_dir = ""
        self.theme_manager = ThemeManager()
        self.language_manager = LanguageManager()
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(self.language_manager.get_text("window_title"))
        self.setMinimumSize(600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        dir_group = QGroupBox(self.language_manager.get_text("directories"))
        dir_layout = QVBoxLayout(dir_group)

        source_layout = QHBoxLayout()
        source_label = QLabel(self.language_manager.get_text("source_folder"))
        self.source_path_label = QLabel(self.language_manager.get_text("no_folder_selected"))
        self.source_path_label.setStyleSheet("font-style: italic;")
        source_btn = QPushButton(self.language_manager.get_text("select_button"))
        source_btn.clicked.connect(self.select_source_dir)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_path_label, 1)
        source_layout.addWidget(source_btn)

        target_layout = QHBoxLayout()
        target_label = QLabel(self.language_manager.get_text("target_folder"))
        self.target_path_label = QLabel(self.language_manager.get_text("no_folder_selected"))
        self.target_path_label.setStyleSheet("font-style: italic;")
        target_btn = QPushButton(self.language_manager.get_text("select_button"))
        target_btn.clicked.connect(self.select_target_dir)
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_path_label, 1)
        target_layout.addWidget(target_btn)
        dir_layout.addLayout(source_layout)
        dir_layout.addLayout(target_layout)

        config_group = QGroupBox(self.language_manager.get_text("settings"))
        config_layout = QVBoxLayout(config_group)

        lang_layout = QHBoxLayout()
        lang_label = QLabel(self.language_manager.get_text("target_language"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(self.language_manager.get_text("portuguese") + " (Brasil)", "pt")
        self.lang_combo.addItem(self.language_manager.get_text("english"), "en")
        self.lang_combo.addItem("Español", "es")
        self.lang_combo.addItem("Français", "fr")
        self.lang_combo.addItem("Deutsch", "de")
        self.lang_combo.addItem("Italiano", "it")

        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo, 1)

        ui_lang_layout = QHBoxLayout()
        ui_lang_label = QLabel(self.language_manager.get_text("interface_language"))
        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItem(self.language_manager.get_text("portuguese"), "pt-br")
        self.ui_lang_combo.addItem(self.language_manager.get_text("english"), "en")
        self.ui_lang_combo.currentIndexChanged.connect(self.change_interface_language)
        ui_lang_layout.addWidget(ui_lang_label)
        ui_lang_layout.addWidget(self.ui_lang_combo, 1)

        theme_layout = QHBoxLayout()
        theme_label = QLabel(self.language_manager.get_text("theme"))
        self.theme_checkbox = QCheckBox(self.language_manager.get_text("dark_mode"))
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_checkbox, 1)
        config_layout.addLayout(lang_layout)
        config_layout.addLayout(ui_lang_layout)
        config_layout.addLayout(theme_layout)

        progress_layout = QVBoxLayout()
        self.progress_label = QLabel(self.language_manager.get_text("progress"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)

        action_layout = QHBoxLayout()
        self.translate_btn = QPushButton(self.language_manager.get_text("translate_button"))
        self.translate_btn.clicked.connect(self.start_translation)
        self.translate_btn.setEnabled(False)
        action_layout.addStretch()
        action_layout.addWidget(self.translate_btn)

        main_layout.addWidget(dir_group)
        main_layout.addWidget(config_group)
        main_layout.addLayout(progress_layout)
        main_layout.addLayout(action_layout)

        self.apply_theme()
    

    def select_source_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, self.language_manager.get_text("select_source"))
        if dir_path:
            self.source_dir = dir_path
            self.source_path_label.setText(dir_path)

            has_html_xml = self.check_for_html_xml_files(dir_path)
            if not has_html_xml:
                QMessageBox.warning(
                    self, 
                    self.language_manager.get_text("warning"), 
                    self.language_manager.get_text("no_html_xml")
                )
            self.update_translate_button()
            
    def check_for_html_xml_files(self, directory):
        """Verifica se o diretório contém arquivos HTML ou XML."""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.html', '.htm', '.xml')):
                    return True
        return False
        
    def select_target_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, self.language_manager.get_text("select_target"))
        if dir_path:
            self.target_dir = dir_path
            self.target_path_label.setText(dir_path)
            self.update_translate_button()
            
    def update_translate_button(self):
        self.translate_btn.setEnabled(bool(self.source_dir and self.target_dir))
        
    def toggle_theme(self, state):
        self.theme_manager.set_dark_mode(state == 2) 
        self.apply_theme()
        
    def apply_theme(self):
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
        
    def change_interface_language(self, index):
            try:
                language_code = self.ui_lang_combo.itemData(index)
                self.language_manager.set_language(language_code)
                self.update_ui_texts()
            except Exception as e:
                print(f"Error changing language: {str(e)}")

                prev_index = 0 if index == 1 else 1 
                self.ui_lang_combo.setCurrentIndex(prev_index)
    def update_ui_texts(self):
            try:

                self.setWindowTitle(self.language_manager.get_text("window_title"))

                try:
                    dir_group = self.findChild(QGroupBox, name="directories")
                    if dir_group and isinstance(dir_group, QGroupBox):
                        dir_group.setTitle(self.language_manager.get_text("directories"))
                    
                    settings_group = self.findChild(QGroupBox, name="settings")
                    if settings_group and isinstance(settings_group, QGroupBox):
                        settings_group.setTitle(self.language_manager.get_text("settings"))
                except Exception as e:
                    print(f"Error updating group boxes: {str(e)}")

                try:
                    self.progress_label.setText(self.language_manager.get_text("progress"))
                except AttributeError:
                    pass

                try:
                    self.translate_btn.setText(self.language_manager.get_text("translate_button"))
                except AttributeError:
                    pass

                try:
                    self.theme_checkbox.setText(self.language_manager.get_text("dark_mode"))
                except AttributeError:
                    pass

                buttons = self.findChildren(QPushButton)
                for button in buttons:
                    try:
                        if button != self.translate_btn and isinstance(button, QPushButton):
                            if "Select" in button.text() or "Selecionar" in button.text():
                                button.setText(self.language_manager.get_text("select_button"))
                    except AttributeError:
                        continue

                if self.source_dir == "":
                    try:
                        self.source_path_label.setText(self.language_manager.get_text("no_folder_selected"))
                    except AttributeError:
                        pass
                if self.target_dir == "":
                    try:
                        self.target_path_label.setText(self.language_manager.get_text("no_folder_selected"))
                    except AttributeError:
                        pass

                labels = self.findChildren(QLabel)
                for label in labels:
                    if label == self.source_path_label or label == self.target_path_label or label == self.progress_label:
                        continue
                    try:
                        if isinstance(label, QLabel):
                            text = label.text().lower()
                            if any(x in text for x in ["source", "origem"]):
                                label.setText(self.language_manager.get_text("source_folder"))
                            elif any(x in text for x in ["target folder", "pasta de destino"]):
                                label.setText(self.language_manager.get_text("target_folder"))
                            elif any(x in text for x in ["target language", "idioma de destino"]):
                                label.setText(self.language_manager.get_text("target_language"))
                            elif any(x in text for x in ["interface language", "idioma da interface"]):
                                label.setText(self.language_manager.get_text("interface_language"))
                            elif any(x in text for x in ["theme", "tema"]):
                                label.setText(self.language_manager.get_text("theme"))
                    except (AttributeError, TypeError):
                        continue

                current_target_lang = self.lang_combo.currentData()
                current_ui_lang = self.ui_lang_combo.currentData()

                self.lang_combo.clear()
                self.lang_combo.addItem(self.language_manager.get_text("portuguese") + " (Brasil)", "pt")
                self.lang_combo.addItem(self.language_manager.get_text("english"), "en")
                self.lang_combo.addItem(self.language_manager.get_text("spanish"), "es")
                self.lang_combo.addItem(self.language_manager.get_text("french"), "fr")
                self.lang_combo.addItem(self.language_manager.get_text("german"), "de")
                self.lang_combo.addItem(self.language_manager.get_text("italian"), "it")

                index = self.lang_combo.findData(current_target_lang)
                if index >= 0:
                    self.lang_combo.setCurrentIndex(index)

                self.ui_lang_combo.blockSignals(True)  
                self.ui_lang_combo.clear()
                self.ui_lang_combo.addItem(self.language_manager.get_text("portuguese"), "pt-br")
                self.ui_lang_combo.addItem(self.language_manager.get_text("english"), "en")

                index = self.ui_lang_combo.findData(current_ui_lang)
                if index >= 0:
                    self.ui_lang_combo.setCurrentIndex(index)
                self.ui_lang_combo.blockSignals(False)  
            except Exception as e:
                print(f"Error updating UI texts: {str(e)}")
    def start_translation(self):
            if not self.source_dir or not self.target_dir:
                QMessageBox.warning(
                    self, 
                    self.language_manager.get_text("warning"), 
                    self.language_manager.get_text("select_folders")
                )
                return
            target_language = self.lang_combo.currentData()

            self.translate_btn.setEnabled(False)
            self.progress_bar.setValue(0)

            self.translation_thread = TranslationThread(
                self.source_dir, 
                self.target_dir, 
                target_language
            )
            self.translation_thread.progress_signal.connect(self.update_progress)
            self.translation_thread.finished_signal.connect(self.translation_finished)
            self.translation_thread.start()
    def update_progress(self, value):
            self.progress_bar.setValue(value)
    def translation_finished(self, success, message):
            self.translate_btn.setEnabled(True)
            
            if success:
                QMessageBox.information(
                    self, 
                    self.language_manager.get_text("success"), 
                    self.language_manager.get_text("translation_complete")
                )
            else:
                QMessageBox.critical(
                    self, 
                    self.language_manager.get_text("error"), 
                    message
                )