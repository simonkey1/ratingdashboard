# Contribuyendo a Rating Scraper

¡Gracias por tu interés en contribuir! 🎉

## Código de Conducta

Este proyecto sigue el [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Al participar, se espera que mantengas este código.

## ¿Cómo Puedo Contribuir?

### Reportar Bugs

Si encuentras un bug, por favor abre un [issue](https://github.com/tuusuario/rating_scraping/issues) con:

- **Título descriptivo**
- **Pasos para reproducir** el bug
- **Comportamiento esperado** vs **comportamiento actual**
- **Screenshots** si aplica
- **Versión de Python** y sistema operativo

### Sugerir Mejoras

Las sugerencias son bienvenidas! Abre un [issue](https://github.com/tuusuario/rating_scraping/issues) con:

- **Descripción clara** de la mejora
- **Casos de uso** donde sería útil
- **Ejemplos** si es posible

### Pull Requests

1. **Fork** el repositorio
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Haz tus cambios** siguiendo las guías de estilo
4. **Commit** tus cambios:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
5. **Push** a tu fork:
   ```bash
   git push origin feature/AmazingFeature
   ```
6. **Abre un Pull Request**

## Guías de Estilo

### Python

- Seguir [PEP 8](https://pep8.org/)
- Usar type hints cuando sea posible
- Docstrings en formato Google
- Máximo 100 caracteres por línea

### Git Commits

- Usar presente: "Add feature" no "Added feature"
- Primera línea: resumen de 50 caracteres
- Cuerpo del commit: explicación detallada si es necesario

### Documentación

- Actualizar README.md si cambias funcionalidad
- Agregar docstrings a funciones nuevas
- Actualizar DEPLOYMENT.md si cambias deployment

## Estructura del Proyecto

```
rating_scraping/
├── src/           # Código fuente
├── scripts/       # Scripts de utilidad
├── docs/          # Documentación
└── .github/       # GitHub config
```

## Testing

Antes de hacer PR, verifica que:

```bash
# Test de scraping
python scripts/test_scraper.py

# Verificar que el dashboard carga
streamlit run src/dashboard.py
```

## Preguntas

¿Tienes preguntas? Abre un [issue](https://github.com/tuusuario/rating_scraping/issues) o contacta al maintainer.

¡Gracias por contribuir! 🚀
