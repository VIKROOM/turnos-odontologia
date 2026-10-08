from app.main import app


def _rutas(root):
    for ruta in root:
        if hasattr(ruta, "path"):
            yield ruta.path
        anidadas = getattr(ruta, "routes", None)
        if anidadas:
            yield from _rutas(anidadas)


def test_app_exposes_healthz_route() -> None:
    assert "/healthz" in _rutas(app.routes)
