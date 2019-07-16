import os
import gettext

class LanguageManagement(object):
    def __init__(self, locales_folder=None, lang=None, file=None):
        self.locales_folder = locales_folder
        if lang == None:
            if "LANGUAGE" in os.environ:
                lang = os.environ['LANGUAGE']
        else:
            os.environ['LANGUAGE'] = lang
        self.default_language = lang

        self.current_language = lang
        self.available_languages = { "en": "english", "fr": "french" }
        self.detailed_languages = { "en": "en_US", "fr": "fr_FR" }
        self.translation_obj = {}

        if lang != None and file != None and locales_folder != None:
            self.translation_obj[file] = gettext.translation(
                domain=file, localedir=self.locales_folder,
                fallback=True, languages=[lang])
            self.translation_obj[file].install()

    def set_locales_folder(self, locales_folder):
        self.locales_folder = locales_folder

    def get_detailed_locale(self, locale):
        return self.detailed_languages[locale]

    def get_detailed_locale_country(self, locale):
        locale_detailed = self.detailed_languages[locale]
        begin = locale_detailed.find('_') + 1
        end = len(locale_detailed)
        if begin <= 0:
            return None
        return locale_detailed[begin:end]

    def get_all_languages(self):
        return self.available_languages

    def get_current_language(self):
        return self.current_language

    def change_language_file(self, lang, file):
        if lang in self.available_languages.keys():
            code = lang
        else:
            code = self.default_language

        self.current_language = code
      
        self.translation_obj[file] = gettext.translation(
            domain=file, localedir=self.locales_folder,
            fallback=True, languages=[code])
        self.translation_obj[file].install()

    def change_language_all_files(self, lang):
        if lang in self.available_languages.keys():
            code = lang
        else:
            code = self.default_language

        self.current_language = code
      
        for current_file in self.translation_obj.keys():
            self.translation_obj[current_file] = gettext.translation(
                domain=current_file, localedir=self.locales_folder,
                fallback=True, languages=[code])
            self.translation_obj[current_file].install()

    def print_in_lang(self, file, id):
        if not self.translation_obj or not self.translation_obj[file]:
            self.translation_obj[file] = gettext.translation(
                domain=file, localedir=self.locales_folder,
                fallback=True, languages=[self.current_language])
            self.translation_obj[file].install()
        return self.translation_obj[file].gettext(id)