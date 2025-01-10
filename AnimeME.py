import errors as error
from BackInfo import AnimeResult,AnimeFindResult,AnimeMpdFile,AnimeTranslationID
try: import lxml; _LXML = True
except ImportError as e: _LXML = False;_LXML_ERROR = e


class parser:
    @staticmethod
    def find_anime(query:str, use_lxml:bool = False) -> AnimeResult:
        if not _LXML and use_lxml:
            raise error.LxmlUseError(
                f'Хотя lxml включён, возникла ошибка: {str(_LXML_ERROR)}. '
                'Пожалуйста, проверьте установку пакета lxml.'
            )
        elif use_lxml: LXML = 'lxml'
        else: LXML = 'html.parser'
        return AnimeResult(query,LXML)
        
    def get_info(link:str, use_lxml:bool = False) -> dict:
        if not _LXML and use_lxml: raise error.LxmlUseError(f'Хотя lxml включён, возникла ошибка: {str(_LXML_ERROR)}. ''Пожалуйста, проверьте установку пакета lxml.')
        elif use_lxml: LXML = 'lxml'
        else: LXML = 'html.parser'
        return AnimeFindResult.res(link,LXML)
    
    def get_mpd(id:str,episode:str,translation_id:str,use_lxml:bool = False) -> str:
        if not _LXML and use_lxml: raise error.LxmlUseError(f'Хотя lxml включён, возникла ошибка: {str(_LXML_ERROR)}. ''Пожалуйста, проверьте установку пакета lxml.')
        elif use_lxml: LXML = 'lxml'
        else: LXML = 'html.parser'
        return AnimeMpdFile.get(id,episode,translation_id,LXML)
    
    def get_translation_id(id:str|int, use_lxml:bool = False) -> dict:
        if not _LXML and use_lxml: raise error.LxmlUseError(f'Хотя lxml включён, возникла ошибка: {str(_LXML_ERROR)}. ''Пожалуйста, проверьте установку пакета lxml.')
        elif use_lxml: LXML = 'lxml'
        else: LXML = 'html.parser'
        return AnimeTranslationID.get_all_TranslationID(id,LXML)
        
    def get_anime_id(link:str):
        val = ''
        for i in link[::-1]:
            try: int(i);val += i
            except Exception: return val[::-1]

