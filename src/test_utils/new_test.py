from jqbx_api import JQBXAPI, AbstractJQBXAPI

JQBX_API: AbstractJQBXAPI = JQBXAPI()

print(JQBX_API.roomsActive(0))