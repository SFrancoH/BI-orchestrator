from .connection import _get, BASE_URL

def list_properties(object_type="contacts"):
    url = f"{BASE_URL}/crm/v3/properties/{object_type}"
    try:
        results = _get(url).get("results", [])
        print(f"\n🔍 Propiedades para '{object_type}':")
        for p in results:
            print(f"• {p['name']:<30} | {p.get('label','sin etiqueta'):<30} | Grupo: {p.get('groupName')}")
        return results
    except Exception as e:
        print("⚠️ Error listando propiedades:", e)
        return []

def list_properties_by_group(object_type="contacts", group_name=None):
    props = list_properties(object_type)
    filtered = [p for p in props if p.get("groupName") == group_name]
    if not filtered:
        print(f"⚠️ No props en grupo '{group_name}' para '{object_type}'")
    else:
        print(f"\n🔍 Props de '{object_type}' en grupo '{group_name}':")
        for p in filtered:
            print(f"• {p['name']:<30} | {p.get('label','sin etiqueta')}")
    return filtered
