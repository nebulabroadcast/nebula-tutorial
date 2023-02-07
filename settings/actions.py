from nebula.settings.models import ActionSettings

def load_setting(name):
    return open(f"/settings/actions/{name}.xml").read()
    
    

ACTIONS = [ActionSettings(id=1, name="proxy", type="conv", settings=load_setting("proxy"))]
