import os
import gettext


class LanguageManagement(object):
    def __init__(self, config=None, file=None):
        lang = config['default_language_code']
        self.locales_folder = config['locales_folder']
        if lang is None and 'LANGUAGE' in os.environ:
            lang = os.environ['LANGUAGE']
        else:
            lang = 'en'
        self.default_language = lang

        self.current_language = lang
        self.available_languages = {'en': 'english', 'fr': 'french'}
        self.detailed_languages = {'en': 'en_US', 'fr': 'fr_FR'}
        self.translater = {}

        if lang is not None and file is not None and self.locales_folder is not None:
            self.translater[file] = gettext.translation(
                domain=file, localedir=self.locales_folder,
                fallback=True, languages=[lang])
            self.translater[file].install()

    def get_detailed_locale(self, locale):
        return self.detailed_languages[locale]

    def get_detailed_locale_country(self, locale):
        locale_detailed = self.detailed_languages[locale]
        begin = locale_detailed.find('_') + 1
        end = len(locale_detailed)
        if begin <= 0:
            return None
        return locale_detailed[begin:end]

    def change_language_file(self, lang, file):
        code = self.default_language
        if lang in self.available_languages.keys():
            code = lang

        self.current_language = code
        self.translater[file] = gettext.translation(
            domain=file, localedir=self.locales_folder,
            fallback=True, languages=[code])
        self.translater[file].install()

    def change_language_all_files(self, lang):
        code = self.default_language
        if lang in self.available_languages.keys():
            code = lang

        self.current_language = code
        for current_file in self.translater.keys():
            self.translater[current_file] = gettext.translation(
                domain=current_file, localedir=self.locales_folder,
                fallback=True, languages=[code])
            self.translater[current_file].install()

    def translate_msg(self, file, message_name):
        if not self.translater or not self.translater[file]:
            self.translater[file] = gettext.translation(
                domain=file, localedir=self.locales_folder,
                fallback=True, languages=[self.current_language])
            self.translater[file].install()
        return self.translater[file].gettext(message_name)
