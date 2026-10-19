# Recursos de LabSim que usa el armado

Copia de lo que el libro toma del repositorio de LabSim para **armarse** sin él
(se sacó de LabSim el 2026-10-19):

- `docs/manual/fuentes/`: tipografías del libro.
- `docs/manual/capturas/casos_demo.json`: los pacientes de práctica 33-42.
- `docs/manual/img/...`: las capturas de LabSim que citan los capítulos
  (rutas `/docs/manual/...` en los `.md`).

Para **rearmar casos o figuras del motor** sí hace falta un checkout de LabSim
(`src/`, `labsim_backend/`): por defecto `../LabSim`, o el que diga la variable
`LABSIM`. Si una captura nueva de LabSim entra al libro, se copia acá con la
misma ruta.
