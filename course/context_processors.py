from yapayarsiv.settings import general_settings_cache_path
import json
def loadSettings(request):

    with open(str(general_settings_cache_path),'r',encoding='utf-8') as f:
        get_general_settings = json.load(f)
    return {'get_general_settings':get_general_settings,}