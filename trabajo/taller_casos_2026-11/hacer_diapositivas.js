// Genera diapositivas_taller.pptx. Uso:
//   NODE_PATH=<carpeta con node_modules> node hacer_diapositivas.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME);

const IMG = (f) => path.join(__dirname, "img", f);
const OUT = path.join(__dirname, "diapositivas_taller.pptx");

const THEME = {
  name: "Taller ORL",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2A37", lt1: "FFFFFF", dk2: "17324D", lt2: "EEF2F6",
    accent1: "2F7D5B", accent2: "8A3B8F", accent3: "E9B949", accent4: "C2453A",
    accent5: "2B6CB0", accent6: "5A6676", hlink: "2B6CB0", folHlink: "8A3B8F",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13,333 × 7,5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Taller de casos clínicos ORL";
pres.author = "Taller ORL";
const C = pres.SchemeColor;

const W = 13.333, M = 0.6, CW = W - 2 * M;
const Y0 = 1.75, YMAX = 6.95; // área de contenido

// ---------- Layouts ----------
const eyebrowPh = (color) => ({ placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 0.32, w: CW, h: 0.4, fontSize: 14, bold: true, color, charSpacing: 2, margin: 0, valign: "middle" }, text: "" } });
const titlePh = (color, y = 0.72, size = 32) => ({ placeholder: { options: { name: "title", type: "title", x: M, y, w: CW, h: 0.85, fontSize: size, bold: true, color, fontFace: "Cambria", margin: 0, valign: "middle", align: "left" }, text: "" } });

pres.defineSlideMaster({ title: "PORTADA", background: { color: C.text2 }, objects: [
  { placeholder: { options: { name: "eyebrow", type: "body", x: M + 0.2, y: 1.6, w: 11, h: 0.5, fontSize: 18, bold: true, color: C.accent3, charSpacing: 3, margin: 0 }, text: "" } },
  { placeholder: { options: { name: "title", type: "title", x: M + 0.2, y: 2.15, w: 11.5, h: 1.9, fontSize: 52, bold: true, color: C.background1, fontFace: "Cambria", margin: 0, valign: "top", align: "left" }, text: "" } },
]});
pres.defineSlideMaster({ title: "FICHA", background: { color: C.text2 }, objects: [] });
pres.defineSlideMaster({ title: "PAUSA", background: { color: C.accent3 }, objects: [eyebrowPh(C.text2), titlePh(C.text2)] });
pres.defineSlideMaster({ title: "CONTENIDO", background: { color: C.background1 }, objects: [eyebrowPh(C.accent6), titlePh(C.text2)],
  slideNumber: { x: W - M - 0.6, y: 7.05, w: 0.6, h: 0.3, fontSize: 11, color: C.accent6, align: "right" } });
pres.defineSlideMaster({ title: "CIERRE", background: { color: C.background2 }, objects: [eyebrowPh(C.accent6), titlePh(C.text2)],
  slideNumber: { x: W - M - 0.6, y: 7.05, w: 0.6, h: 0.3, fontSize: 11, color: C.accent6, align: "right" } });

// ---------- Ayudas ----------
const CASOS = {
  1: { tag: "CASO 1 · ESPIROMETRÍA", col: C.accent5, light: "A9C8EC" },
  2: { tag: "CASO 2 · NARIZ", col: C.accent1, light: "9FD3B8" },
  3: { tag: "CASO 3 · AUDIO Y ELECTROFISIOLOGÍA", col: C.accent2, light: "D9B3DC" },
  4: { tag: "CASO 4 · AUDIO Y ELECTROFISIOLOGÍA", col: C.accent2, light: "D9B3DC" },
};
let section = "";
function nueva(layout, sec) {
  if (sec && sec !== section) { pres.addSection({ title: sec }); section = sec; }
  return pres.addSlide({ masterName: layout, sectionTitle: section });
}
function cabecera(s, eyebrow, titulo, color) {
  s.addText([{ text: eyebrow, options: color ? { color } : {} }], { placeholder: "eyebrow" });
  s.addText(titulo, { placeholder: "title" });
}
// lista de puntos con negrita inicial: [["FND 0,53", " sobre 0,4"], ...]
function puntos(items, size = 16) {
  return items.map((it, i) => {
    const runs = Array.isArray(it) ? it : [null, it];
    const out = [];
    if (runs[0]) out.push({ text: runs[0], options: { bold: true, color: C.text2 } });
    out.push({ text: runs[1], options: { breakLine: i < items.length - 1 } });
    out[0].options.bullet = { indent: 18 };
    out[0].options.paraSpaceAfter = 8;
    return out;
  }).flat();
}
function tarjeta(s, x, y, w, h, fill = C.background2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.12 });
}
// imagen ajustada a una caja, centrada
function imagen(s, file, pw, ph, x, y, w, h, alt) {
  const r = Math.min(w / pw, h / ph);
  const iw = pw * r, ih = ph * r;
  s.addImage({ path: IMG(file), x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: alt });
}
const SZ = {
  "cap35-rs-desv-rm.png": [1400, 938], "cap35-rs-desv-ra.png": [1400, 798],
  "cap36-rs-medic-rm.png": [1400, 938], "cap36-rs-medic-ra.png": [1400, 798],
  "cap11_schwannoma_audiosupra.png": [1455, 762], "cap11_schwannoma_impedancia.png": [938, 424],
  "cap11_schwannoma_abr.png": [1404, 766], "cap11_schwannoma_abr_2.png": [796, 577], "cap11_schwannoma_vemp.png": [1132, 500],
  "cap13_neuropatia_audiosupra.png": [1455, 721], "cap13_neuropatia_logoaudiometria.png": [608, 424],
  "cap13_neuropatia_impedancia.png": [938, 424], "cap13_neuropatia_teoae.png": [1092, 396], "cap13_neuropatia_dpoae.png": [1092, 396],
  "cap13_neuropatia_abr.png": [1404, 577], "cap13_neuropatia_abr_2.png": [1404, 318], "cap13_neuropatia_abr_3.png": [1404, 318],
  "cap13_neuropatia_cortical.png": [1564, 348],
  "cap37-espiro-curvas.png": [1280, 495], "cap37-espiro-tabla.png": [1280, 285],
};
const fig = (s, f, x, y, w, h, alt) => imagen(s, f, SZ[f][0], SZ[f][1], x, y, w, h, alt);

// Figura grande a la izquierda + tarjeta de puntos a la derecha
function slideFigura(n, sec, titulo, f, alt, items, notas, figW = 7.9) {
  const s = nueva("CONTENIDO", sec);
  cabecera(s, CASOS[n].tag + " · RESULTADOS", titulo, CASOS[n].col);
  fig(s, f, M, Y0, figW, YMAX - Y0, alt);
  const x = M + figW + 0.35, w = W - M - x;
  tarjeta(s, x, Y0, w, YMAX - Y0);
  s.addText(puntos(items), { x: x + 0.25, y: Y0 + 0.2, w: w - 0.5, h: YMAX - Y0 - 0.4, fontSize: 16, color: C.text1, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes(notas);
  return s;
}
function slideFicha(n, sec, rostro, nombre, datos, cita, notas) {
  const s = nueva("FICHA", sec);
  s.addImage({ path: IMG(rostro), x: M + 0.2, y: 1.3, w: 4.6, h: 4.6, altText: "Retrato de " + nombre + " (rostro generado con IA)" });
  const x = M + 5.3, w = W - M - x;
  s.addText(CASOS[n].tag, { x, y: 1.3, w, h: 0.4, fontSize: 15, bold: true, color: CASOS[n].light, charSpacing: 2, margin: 0, isTextBox: true });
  s.addText(nombre, { x, y: 1.75, w, h: 0.9, fontSize: 40, bold: true, fontFace: "Cambria", color: C.background1, margin: 0, isTextBox: true });
  s.addText(datos, { x, y: 2.7, w, h: 1.3, fontSize: 16, color: "C9D6E3", margin: 0, valign: "top", isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.15, w, h: 1.75, fill: { color: "234466" }, line: { color: "234466" }, rectRadius: 0.12 });
  s.addText(cita, { x: x + 0.3, y: 4.25, w: w - 0.6, h: 1.55, fontSize: 18, italic: true, fontFace: "Cambria", color: C.background1, margin: 0, valign: "middle", isTextBox: true });
  s.addNotes(notas);
}
function slidePausa(n, sec, etapa, titulo, preguntas, notas) {
  const s = nueva("PAUSA", sec);
  const tag = n ? CASOS[n].tag.split(" · ")[0] + " · " : "";
  cabecera(s, tag + etapa, titulo);
  const fs = preguntas.length > 5 ? 21 : 24;
  s.addText(preguntas.map((q, i) => [
    { text: (i + 1) + ".  ", options: { bold: true } },
    { text: q, options: { breakLine: i < preguntas.length - 1 } }]).flat()
    .map((r, k) => (k % 2 === 0 ? Object.assign(r, { options: Object.assign(r.options, { indent: 0, paraSpaceAfter: 14 }) }) : r)),
    { x: M, y: Y0 + 0.1, w: CW, h: YMAX - Y0 - 0.1, fontSize: fs, color: C.text2, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes(notas);
}
function slideCierre(n, sec, conclusion, cards, notas) {
  const s = nueva("CIERRE", sec);
  cabecera(s, CASOS[n].tag + " · CIERRE", conclusion, CASOS[n].col);
  const gap = 0.35, cw = (CW - gap * (cards.length - 1)) / cards.length;
  cards.forEach(([big, txt], i) => {
    const x = M + i * (cw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.3, w: cw, h: 4.2, fill: { color: C.background1 }, line: { color: "D5DDE6" }, rectRadius: 0.12 });
    s.addText(big, { x: x + 0.3, y: 2.55, w: cw - 0.6, h: 1.3, fontSize: 30, bold: true, fontFace: "Cambria", color: CASOS[n].col, margin: 0, valign: "top", isTextBox: true });
    s.addText(txt, { x: x + 0.3, y: 3.95, w: cw - 0.6, h: 2.35, fontSize: 17, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  });
  s.addNotes(notas);
}
function tabla(rows, opts) {
  const head = { bold: true, color: C.text2, fill: { color: C.background2 } };
  return rows.map((r, i) => r.map((c, j) => ({ text: String(c), options: Object.assign({ align: j === 0 ? "left" : "center", valign: "middle" }, i === 0 ? head : {}, (opts.bold || []).some(([a, b]) => a === i && b === j) ? { bold: true, color: C.accent4 } : {}) })));
}
const TB = { fontSize: 15, color: C.text1, border: { type: "solid", pt: 0.75, color: "C9D3DD" }, margin: 0.06 };

// =====================================================================
// Portada y dinámica
// =====================================================================
{
  const s = nueva("PORTADA", "Presentación");
  s.addText("TALLER DE CASOS CLÍNICOS", { placeholder: "eyebrow" });
  s.addText("Vía aérea, audiología y electrofisiología", { placeholder: "title" });
  s.addText("Cuatro pacientes para razonar en grupo: de la historia a la hipótesis, de la hipótesis al examen, del examen al informe.",
    { x: M + 0.2, y: 4.1, w: 9.5, h: 0.9, fontSize: 20, color: "C9D6E3", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M + 0.2, y: 5.2, w: 2.6, h: 0.5, fill: { color: "A9C8EC" }, line: { color: "A9C8EC" }, rectRadius: 0.25 });
  s.addText("1 de espirometría", { x: M + 0.2, y: 5.2, w: 2.6, h: 0.5, fontSize: 15, bold: true, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M + 3.0, y: 5.2, w: 1.9, h: 0.5, fill: { color: "9FD3B8" }, line: { color: "9FD3B8" }, rectRadius: 0.25 });
  s.addText("1 de nariz", { x: M + 3.0, y: 5.2, w: 1.9, h: 0.5, fontSize: 15, bold: true, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M + 5.1, y: 5.2, w: 4.6, h: 0.5, fill: { color: "D9B3DC" }, line: { color: "D9B3DC" }, rectRadius: 0.25 });
  s.addText("2 casos de audio y electrofisiología", { x: M + 5.1, y: 5.2, w: 4.6, h: 0.5, fontSize: 15, bold: true, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Casos 37.2, 36.2, 11.1 y 13.1 de «Evaluación y rehabilitación en otorrinolaringología». Pacientes ficticios; rostros generados con IA.",
    { x: M + 0.2, y: 6.75, w: 11, h: 0.4, fontSize: 12, color: "8FA6BC", margin: 0, isTextBox: true });
  s.addNotes("Presentar el taller: cuatro casos del libro, uno de espirometría, uno de nariz y dos de audio y electrofisiología. Cada caso tiene dos etapas: primero solo la historia, después los resultados. Los estudiantes trabajan con el cuadernillo impreso.");
}
{
  const s = nueva("CONTENIDO", "Presentación");
  cabecera(s, "DINÁMICA", "Cómo trabajamos");
  const pasos = [["Paso 1", "¿Qué datos importan?", "Lo que el relato dice y lo que no dice."],
    ["Paso 2", "Hipótesis", "Cada una con el dato que la apoya o la descarta."],
    ["Paso 3", "¿Qué pedirían?", "Qué examen, en qué orden y qué esperan encontrar."],
    ["Paso 4", "Resultados", "Interpretar y redactar la conclusión del informe."]];
  const gap = 0.3, cw = (CW - 3 * gap) / 4;
  pasos.forEach(([a, b, c], i) => {
    const x = M + i * (cw + gap);
    tarjeta(s, x, Y0, cw, 2.4, i < 3 ? C.background2 : "FBF1DA");
    s.addText(a.toUpperCase(), { x: x + 0.25, y: Y0 + 0.2, w: cw - 0.5, h: 0.35, fontSize: 13, bold: true, color: i < 3 ? C.accent6 : "8A5A00", charSpacing: 2, margin: 0, isTextBox: true });
    s.addText(b, { x: x + 0.25, y: Y0 + 0.6, w: cw - 0.5, h: 0.6, fontSize: 21, bold: true, fontFace: "Cambria", color: C.text2, margin: 0, isTextBox: true });
    s.addText(c, { x: x + 0.25, y: Y0 + 1.3, w: cw - 0.5, h: 0.9, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  });
  s.addText("Etapa 1 (solo la historia)", { x: M, y: Y0 + 2.5, w: 3 * cw + 2 * gap, h: 0.35, fontSize: 13, color: C.accent6, align: "center", margin: 0, isTextBox: true });
  s.addText("Etapa 2", { x: M + 3 * (cw + gap), y: Y0 + 2.5, w: cw, h: 0.35, fontSize: 13, color: "8A5A00", align: "center", margin: 0, isTextBox: true });
  const half = (CW - 0.5) / 2;
  s.addText([{ text: "Grupos de 4 o 5, con roles que rotan", options: { bold: true, color: C.text2, breakLine: true, fontSize: 18 } },
    { text: "Coordinador/a (tiempo y que hablen todos), secretario/a (escribe) y vocero/a (presenta)." }],
    { x: M, y: 5.1, w: half, h: 1.4, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addText([{ text: "El informe describe un patrón", options: { bold: true, color: C.text2, breakLine: true, fontSize: 18 } },
    { text: "El diagnóstico y el tratamiento son del médico. Cada decisión se justifica con un dato del caso." }],
    { x: M + half + 0.5, y: 5.1, w: half, h: 1.4, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Los pasos 1 a 3 son la Etapa 1. El paso 4 es la Etapa 2 y se abre cuando el docente muestra los resultados. Pedir que no den vuelta la página del cuadernillo antes de tiempo. Unos 25 minutos por caso.");
}

// =====================================================================
// CASO 1 · Verónica
// =====================================================================
const S1 = "Caso 1 · Verónica";
slideFicha(1, S1, "rostro_cap37_estenosis.jpg", "Verónica, 49 años",
  "Secretaria, nunca fumó. Hace 14 meses, neumonía grave: 12 días con ventilación mecánica por tubo en la tráquea; salió ronca y la voz se normalizó en un mes. Hace 5 meses: «asma», corticoide con formoterol, sin cambio. Sin estornudos, picazón ni alergias.",
  "«Desde hace ocho meses me agito al subir una escalera. Ahora hago ruido al respirar: lo oyen los demás, sobre todo cuando tomo aire.»",
  "Derivada por médico general: disnea que no responde al tratamiento del asma; espirometría con prueba broncodilatadora. Suspendió el formoterol 24 horas antes. Audición normal.");
slidePausa(1, S1, "ETAPA 1 · EN GRUPOS · 7 MIN", "Antes de ver los resultados", [
  "¿Qué dice que el ruido se oiga al inspirar? ¿Qué relación puede tener la intubación de hace 14 meses con lo de ahora?",
  "Causas de disnea progresiva con ruido al respirar que no mejora con el inhalador. ¿Qué hace menos probable el asma?",
  "¿Qué revisan antes de empezar? ¿Qué forma de curva esperan en un asma y cuál si el problema está en la vía aérea alta?",
  "¿Qué mirarían mientras sopla? Si el VEF1 y la razón salen normales, ¿alcanza para decir «espirometría normal»?",
], "Esperado: ruido inspiratorio (estridor) = vía aérea alta. La intubación prolongada es la causa clásica de estenosis laringotraqueal, que aparece meses después al cicatrizar. Hipótesis: asma que no responde, estenosis postintubación, parálisis de cuerdas vocales, obstrucción laríngea inducible, disnea cardíaca. Asma: descenso cóncavo y respuesta al broncodilatador; vía aérea alta: mesetas. La forma de la curva se mira durante el examen.");
slideFigura(1, S1, "La curva flujo-volumen: una caja", "cap37-espiro-curvas.png",
  "Curvas flujo-volumen y volumen-tiempo de Verónica, pre y post broncodilatador", [
    ["Espiración: ", "el flujo sube y se queda en una meseta de 3,2 L/s hasta la mitad de la maniobra."],
    ["Inspiración: ", "también se corta, en 3,0 L/s."],
    ["Tope en los dos sentidos: ", "el estrechamiento es fijo."],
    ["Pre y post se superponen: ", "el broncodilatador no cambia nada."],
  ], "Azul: pre; rojo, rayas: post. Preguntar cómo se vería un asma: pico alto y descenso cóncavo, con la curva post más alta. Ni con la curva se sabe si el estrechamiento está dentro o fuera del tórax: lo resuelve la endoscopía.", 9.2);
{
  const s = nueva("CONTENIDO", S1);
  cabecera(s, CASOS[1].tag + " · RESULTADOS", "Los números: todo «dentro de lo normal»", CASOS[1].col);
  fig(s, "cap37-espiro-tabla.png", M, Y0 - 0.1, CW, 2.75, "Tabla de resultados de la espirometría de Verónica");
  const items = [
    ["78,2 % > 69,7 %", "VEF1/CVF sobre el LIN. VEF1 94 % del teórico, z −0,45. Por la tabla: sin obstrucción."],
    ["13,2 > 8", "VEF1 (2.540 mL) / FEM (3,2 L/s = 192 L/min). Sugiere obstrucción de la vía aérea alta."],
    ["0,7 %", "Cambio del VEF1 con broncodilatador, sobre el teórico: (2,56 − 2,54) / 2,70. Sin respuesta (corte: > 10 %)."],
  ];
  const gap = 0.35, cw = (CW - 2 * gap) / 3, y = 4.85;
  items.forEach(([big, txt], i) => {
    const x = M + i * (cw + gap);
    tarjeta(s, x, y, cw, 1.95);
    s.addText(big, { x: x + 0.25, y: y + 0.15, w: cw - 0.5, h: 0.6, fontSize: 26, bold: true, fontFace: "Cambria", color: CASOS[1].col, margin: 0, isTextBox: true });
    s.addText(txt, { x: x + 0.25, y: y + 0.8, w: cw - 0.5, h: 1.05, fontSize: 14, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  });
  s.addNotes("Primero que lean solo la tabla: una lectura así informaría «espirometría normal». Después que calculen el cociente (ojo: FEM en L/s × 60) y el cambio sobre el teórico. FEF50/FIF50 = 1,07 (normal 0,9-1,1): en una obstrucción fija los dos flujos están igual de limitados y el cociente no la separa de un sano. Curva: más sensible; VEF1/FEM: más específico (Miller y cols., 1990).");
}
slidePausa(1, S1, "ETAPA 2 · EN GRUPOS · 10 MIN", "Interpreten los resultados", [
  "Lean solo la tabla: ¿hay obstrucción según la razón? ¿Qué diría un informe que mirara solo los números?",
  "Describan la curva en espiración e inspiración. ¿Qué significa que el tope aparezca en los dos sentidos?",
  "Calculen VEF1 (mL) / FEM (L/min). ¿Qué punto de corte usa el manual?",
  "Calculen el cambio del VEF1 sobre el teórico. ¿Por qué un estrechamiento así no responde al salbutamol?",
  "FEF50/FIF50 da 1,07, dentro de lo normal. ¿Por qué no sirve aquí?",
  "Redacten la conclusión. ¿Pueden escribir «estenosis traqueal»? ¿A quién avisan y cuándo?",
], "Respuestas en la guía docente, caso 1. Errores esperables: «espirometría normal» por los números; informar «asma»; esperar a repetir la prueba; calcular la respuesta sobre el basal.");
slideCierre(1, S1, "Patrón de obstrucción fija de la vía aérea alta", [
  ["La curva manda", "VEF1 y VEF1/CVF dentro de lo esperado, pero la curva flujo-volumen es una caja: meseta al espirar y al inspirar."],
  ["13,2 y 0,7 %", "VEF1/FEM mayor de 8 y sin respuesta al broncodilatador: no es un asma difícil, es otra cosa hasta demostrar lo contrario."],
  ["Avisar y derivar ya", "Se informa el patrón, no «estenosis». Aviso inmediato al médico; derivación para endoscopía e imagen de la vía aérea."],
], "Informe modelo: volúmenes y razón dentro de lo esperado. Curva flujo-volumen con meseta de flujo en la espiración y en la inspiración, FEM muy bajo y VEF1 (mL)/FEM (L/min) de 13,2: patrón sugerente de obstrucción fija de la vía aérea superior. Sin respuesta al broncodilatador (VEF1 +0,02 L, 0,7 % del teórico). Se recomienda derivación inmediata para evaluación endoscópica y radiológica de la vía aérea. Con un informe «normal» habría seguido otros meses con un inhalador de asma.");

// =====================================================================
// CASO 2 · Álvaro
// =====================================================================
const S2 = "Caso 2 · Álvaro";
slideFicha(2, S2, "rostro_cap36_medicamentosa.jpg", "Álvaro, 29 años",
  "Trabaja en un call center. Hace 8 meses, resfrío fuerte; desde entonces usa un descongestionante en spray comprado sin receta: un frasco por semana, cada 4 a 6 horas. Sin estornudos, picazón ni estación. Sin alergias en la familia. Aguantó 2 días sin el spray para el examen.",
  "«Al principio me duraba toda la noche; ahora me dura dos horas. ¿Después del examen me van a dejar usarlo otra vez?»",
  "Leer el relato completo. Durmió sentado, con la boca seca, y llegó «desesperado». Audición normal.");
slidePausa(2, S2, "ETAPA 1 · EN GRUPOS · 7 MIN", "Antes de ver los resultados", [
  "¿Qué dice que el spray «ahora le dure dos horas»? ¿Y que no tenga estornudos ni cambios con la estación?",
  "Causas de una obstrucción bilateral y constante que empezó con un resfrío: ¿cuál explica que el efecto dure cada vez menos?",
  "¿Qué necesitan saber del spray antes de empezar? ¿Le aplicarían el vasoconstrictor del examen a alguien que lo usa todos los días?",
  "Si hubiera llegado con el spray puesto, ¿qué habrían visto y qué conclusión equivocada podrían escribir?",
], "Esperado: efecto decreciente = taquifilaxia y rebote; sin alergia en el relato. Hipótesis: rinitis por descongestionantes, alérgica persistente, no alérgica, estructural. Con el spray puesto el reposo saldría cerca de 0,28 y la prueba sin cambio: se informaría «estructural» una nariz que es solo mucosa.");
{
  const s = nueva("CONTENIDO", S2);
  cabecera(s, CASOS[2].tag + " · RESULTADOS", "Rinoscopía, rinomanometría y rinometría", CASOS[2].col);
  s.addText([{ text: "Rinoscopía: ", options: { bold: true, color: C.text2 } },
    { text: "cornetes inferiores muy aumentados en las dos fosas, mucosa roja y edematosa, sin secreción; tabique en la línea media; sin pólipos ni masas. " },
    { text: "NOSE 85 (extrema).", options: { bold: true, color: C.accent4 } }],
    { x: M, y: Y0, w: CW, h: 0.75, fontSize: 17, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  const tw = (CW - 0.4) / 2, ty = Y0 + 1.0;
  s.addTable(tabla([["Rinomanometría a 150 Pa", "FND", "FNI", "Total"],
    ["Reposo, inspiración", "2,57", "1,47", "0,93"], ["Reposo, espiración", "2,55", "1,48", ""],
    ["Con VC, inspiración", "0,28", "0,28", "0,14"], ["Con VC, espiración", "0,27", "0,27", ""]],
    { bold: [[1, 1], [1, 2]] }), Object.assign({ x: M, y: ty, w: tw, colW: [2.6, (tw - 2.6) / 3, (tw - 2.6) / 3, (tw - 2.6) / 3], rowH: 0.48 }, TB));
  const x2 = M + tw + 0.4;
  s.addTable(tabla([["Rinometría acústica", "FND", "FND VC", "FNI", "FNI VC"],
    ["MCA1 (cm²) a 1,4 cm", "0,44", "0,69", "0,47", "0,71"], ["MCA2 (cm²) a 3,1 cm", "0,13", "1,88", "0,17", "1,86"],
    ["Volumen 2-5 cm (cm³)", "1,7", "6,8", "2,1", "6,8"]],
    { bold: [[2, 1], [2, 3]] }), Object.assign({ x: x2, y: ty, w: tw, colW: [2.4, (tw - 2.4) / 4, (tw - 2.4) / 4, (tw - 2.4) / 4, (tw - 2.4) / 4], rowH: 0.48 }, TB));
  s.addText("VC: oximetazolina, 2 puff por fosa, medición a los 15 minutos. Rinometría: promedio de tres registros por fosa; en la FND con VC los registros no se parecían entre sí (MCA2 ±0,03 cm²).",
    { x: M, y: 5.6, w: CW, h: 0.7, fontSize: 14, color: C.accent6, margin: 0, isTextBox: true });
  s.addNotes("Calcular: FND (2,57 − 0,28)/2,57 ≈ 89 %; FNI ≈ 81 %. Aquí el total (0,93) sí delata el problema porque las dos fosas están cerradas. Se abrió MCA2: el cornete.");
}
{
  const s = nueva("CONTENIDO", S2);
  cabecera(s, CASOS[2].tag + " · RESULTADOS", "Las curvas: con vasoconstrictor se abre todo", CASOS[2].col);
  const fw = (CW - 0.4) / 2;
  fig(s, "cap36-rs-medic-rm.png", M, Y0, fw, 3.9, "Rinomanometría de Álvaro en reposo y con vasoconstrictor");
  fig(s, "cap36-rs-medic-ra.png", M + fw + 0.4, Y0, fw, 3.9, "Rinometría acústica de Álvaro en reposo y con vasoconstrictor");
  s.addText("Rinomanometría: en reposo las curvas casi no se despegan de la horizontal; con vasoconstrictor (rayas) las dos fosas pasan a unos 530 cm³/s.",
    { x: M, y: Y0 + 4.0, w: fw, h: 1.0, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addText("Rinometría: en reposo los cornetes casi cierran el paso (MCA2 0,13 y 0,17); con vasoconstrictor las dos fosas se superponen.",
    { x: M + fw + 0.4, y: Y0 + 4.0, w: fw, h: 1.0, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Límite del modelo: abre la nariz de Álvaro como abriría la de cualquiera; no tiene taquifilaxia ni curso en el tiempo. En una persona con meses de uso la respuesta puede ser menor.");
}
slidePausa(2, S2, "ETAPA 2 · EN GRUPOS · 10 MIN", "Interpreten los resultados", [
  "Aquí el total es 0,93. ¿Cuándo el total delata el problema y cuándo puede esconderlo (una sola fosa obstruida)?",
  "¿Cuánto bajó cada fosa? ¿Qué tipo de obstrucción es? ¿Qué mínimo de la rinometría se abrió?",
  "Una rinitis alérgica daría la misma respuesta. ¿Qué separa a Álvaro de un alérgico: el equipo u otra cosa?",
  "¿Qué podría ser distinto en un paciente real con meses de uso? ¿Qué hacen con registros que no se repiten?",
  "Redacten la conclusión. ¿Pueden escribir «rinitis medicamentosa»? ¿Dónde queda registrado el spray?",
  "Álvaro quiere volver a usar el spray en la casa. ¿Qué le dicen?",
], "Respuestas en la guía docente, caso 2. Clave: lo que separa a Álvaro de un alérgico es el relato, no la prueba. El uso del spray va en antecedentes del informe y se comunica al médico.");
slideCierre(2, S2, "Obstrucción vasomotora bilateral (mucosa)", [
  ["89 % y 81 %", "Con vasoconstrictor las dos fosas llegan a 0,28 y el cornete se abre (MCA2 de 0,13 a 1,88). Toda la obstrucción es mucosa."],
  ["El relato decide", "La prueba se vería igual en una rinitis alérgica. El antecedente del spray se informa; el diagnóstico es del médico."],
  ["No es un tratamiento", "«La prueba no es un tratamiento; lo que sigue lo decide el médico; no vuelva al producto por su cuenta.»"],
], "Prevención primaria: descongestionantes tópicos solo unos pocos días (no más de 5; Solé y cols., 2025; Dykewicz y cols., 2020). Si el médico confirma, el manejo habitual es retirar el producto con corticoide tópico y tratar la base (Graf, 1997; 2005).");

// =====================================================================
// CASO 3 · Lourdes
// =====================================================================
const S3 = "Caso 3 · Lourdes";
slideFicha(3, S3, "rostro_cap11_schwannoma.jpg", "Lourdes, 52 años",
  "Secretaria en un juzgado. Hace 2 años nota baja audición del oído derecho: el médico general la mandó a observar. Otoscopía normal bilateral. Sin acúfeno. A veces, al darse vuelta rápido en la cama, un mareo de segundos. Losartán 50 mg al día.",
  "«Por el oído derecho oigo, pero no entiendo. Ahora me cambio el celular al izquierdo sin darme cuenta.»",
  "Derivada por otorrinolaringólogo para audiometría e impedanciometría. Nunca ha tenido dolor ni secreción de oídos.");
slidePausa(3, S3, "ETAPA 1 · EN GRUPOS · 7 MIN", "Antes de ver los resultados", [
  "¿Qué dice que «oye pero no entiende» por un solo oído? ¿Y el mareo de segundos al girar en la cama? ¿Y que no tenga acúfeno?",
  "¿Coclear o retrococlear? Anoten qué dato de la historia apoya cada opción.",
  "Armen la batería completa en orden. ¿Qué prueba esperan que separe cóclea de nervio? ¿Dónde necesitarán enmascarar?",
  "Si la pérdida del OD fuera severa en agudos, ¿les servirían los interpicos del PEAT? ¿Qué prueba no depende de la audición?",
], "Esperado: unilateral con mala discriminación = alerta retrococlear. El mareo posicional breve puede ser un VPPB que coexiste. Sin acúfeno no descarta nada. Batería: audiometría con enmascaramiento, logo, supraliminares, impedancia con reflejos y deterioro, PEAT con el OI enmascarado y VEMP.");
slideFigura(3, S3, "Audiometría, logoaudiometría y supraliminares", "cap11_schwannoma_audiosupra.png",
  "Audiograma y tablas de logoaudiometría y supraliminares de Lourdes", [
    ["OD: ", "45 dB en 1 kHz, 95 dB en 4 kHz; ósea pegada a la aérea. OI normal."],
    ["Discriminación OD: ", "no pasa del 20 % (OI: 100 %)."],
    ["SISI 10 %, ", "Carhart con deterioro de 30 dB en 2 y 4 kHz, Metz ausente."],
  ], "Preguntar: con 45 dB en 1 kHz, ¿qué discriminación daría un oído coclear? Bastante más que 20 %. SISI bajo = sin reclutamiento; Carhart = adaptación patológica; Metz no calculable porque no hay reflejo al estimular el OD.", 8.3);
{
  const s = nueva("CONTENIDO", S3);
  cabecera(s, CASOS[3].tag + " · RESULTADOS", "Reflejos: el patrón diagonal", CASOS[3].col);
  fig(s, "cap11_schwannoma_impedancia.png", M, Y0, 6.6, 3.0, "Timpanogramas y reflejos estapediales de Lourdes");
  const tx = M + 7.0, tw = W - M - tx;
  s.addTable(tabla([["Estímulo entra por…", "Sonda OD", "Sonda OI"],
    ["OD", "Ipsi: ausente", "Contra: ausente"], ["OI", "Contra: 90 dB", "Ipsi: 85 dB"]],
    { bold: [[1, 1], [1, 2]] }), Object.assign({ x: tx, y: Y0, w: tw, colW: [2.0, (tw - 2.0) / 2, (tw - 2.0) / 2], rowH: 0.6 }, TB, { fontSize: 16 }));
  s.addText("Falla todo lo que se estimula por el OD, se registre donde se registre: lesión de la rama aferente derecha (VIII par). Si fallara el oído medio derecho, faltaría lo que se registra en el OD.",
    { x: tx, y: Y0 + 2.1, w: tw, h: 1.6, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addText("Timpanogramas normales en los dos oídos: el oído medio no explica los reflejos ausentes.",
    { x: M, y: Y0 + 3.3, w: 6.6, h: 0.8, fontSize: 15, color: C.accent6, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Pedir que dibujen el arco del reflejo en la pizarra y ubiquen la lesión. Valores con 1 kHz.");
}
{
  const s = nueva("CONTENIDO", S3);
  cabecera(s, CASOS[3].tag + " · RESULTADOS", "PEAT: sin onda I, sin interpicos", CASOS[3].col);
  fig(s, "cap11_schwannoma_abr.png", M, Y0, 6.9, 3.9, "PEAT de Lourdes a 80, 60 y 40 dB nHL en los dos oídos");
  const x2 = M + 7.2, w2 = W - M - x2;
  fig(s, "cap11_schwannoma_abr_2.png", x2, Y0, w2, 3.2, "PEAT del oído derecho a 100, 90 y 80 dB nHL con ruido en el izquierdo");
  s.addText("OI: I 1,53 · III 3,67 · V 5,57 ms; I-V 4,04 ms (límite 4,4). OD sin ondas a 80 dB nHL.",
    { x: M, y: Y0 + 4.0, w: 6.9, h: 0.9, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addText("OD con ruido de 55 dB en el OI: a 100 dB III (3,70) y V de baja amplitud; a 90 dB solo V (6,03); a 80 dB nada. Umbral con click: 90 dB nHL.",
    { x: x2, y: Y0 + 3.3, w: w2, h: 1.6, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Ojo: con 70 a 95 dB de pérdida entre 2 y 4 kHz, un click a 80 dB queda casi en el umbral de las frecuencias que usa. Un PEAT sin ondas no basta solo para hablar de nervio. El ruido en el OI evita que el estímulo de 100 dB cruzado responda por el oído sano.");
}
slideFigura(3, S3, "VEMP cervical: el que no depende de la audición", "cap11_schwannoma_vemp.png",
  "VEMP cervical de Lourdes, oído derecho pequeño y oído izquierdo normal", [
    ["OD pequeño: ", "78 µV; corregido por EMG, 1,57."],
    ["OI normal: ", "341 µV; corregido, 6,87."],
    ["Asimetría 63 %, ", "del mismo lado que la pérdida."],
    ["Sáculo y nervio vestibular inferior: ", "informa aunque el umbral ya no deje leer el PEAT."],
  ], "El schwannoma nace del nervio vestibular. El VEMP aporta aunque Lourdes no tenga vértigo. El mareo al girar en la cama no se explica necesariamente por la misma lesión (puede ser un VPPB).", 7.9);
slidePausa(3, S3, "ETAPA 2 · EN GRUPOS · 10 MIN", "Interpreten los resultados", [
  "Con 45 dB en 1 kHz, ¿qué discriminación esperarían de un oído coclear? ¿Qué dice un 20 %?",
  "SISI 10 %, Carhart 30 dB, Metz ausente: ¿qué indica cada uno y hacia dónde apuntan juntos?",
  "Dibujen el arco del reflejo y ubiquen la lesión que explica el patrón diagonal.",
  "¿Por qué se enmascaró el OI al estimular a 100 dB? ¿Qué podría haber pasado sin ruido?",
  "¿Por qué un PEAT sin onda I no basta para decir «nervio»? ¿Qué frecuencias usa el click?",
  "¿Qué aporta el VEMP? Redacten la conclusión y la recomendación.",
], "Respuestas en la guía docente, caso 3. Error esperable: concluir «coclear» porque el PEAT no muestra I ni III, cuando la causa es la pérdida.");
slideCierre(3, S3, "Hipoacusia sensorioneural OD con signos retrococleares", [
  ["El PEAT pierde poder", "Con pérdida severa en agudos, un PEAT sin ondas no separa cóclea de nervio y no hay interpicos que medir."],
  ["Decide la suma", "Discriminación desproporcionada, deterioro tonal, patrón aferente de reflejos y VEMP disminuido del mismo lado."],
  ["Lo que sigue", "Resonancia magnética de conductos auditivos internos con gadolinio."],
], "Informe modelo: OI normal. OD sin ondas a 80 dB nHL; con ruido en OI, III y V de muy baja amplitud a 100 dB y solo V a 90 dB; interpicos no medibles; umbral con click 90 dB nHL (≈ 85 dB eHL). Se sugiere RM de CAI con gadolinio por la discriminación, los reflejos y el VEMP.");

// =====================================================================
// CASO 4 · Esther
// =====================================================================
const S4 = "Caso 4 · Esther";
slideFicha(4, S4, "rostro_cap13_neuropatia.jpg", "Esther, 15 años",
  "Viene con su mamá. Prematura de 33 semanas, 1.900 g; ictericia grave con fototerapia y exanguinotransfusión. Tamizaje auditivo con emisiones: pasó en los dos oídos. Derivada por la profesora jefe: baja de rendimiento, no sigue instrucciones en la sala.",
  "«Oye cuando quiere: hay días en que entiende bien y otros casi nada. Entiende mucho mejor si le ve la cara a quien le habla.»",
  "En la sala, con ruido, se pierde: se sienta adelante y copia del cuaderno de una compañera. En silencio y a solas con su mamá conversa sin problema. Sin acúfeno, dolor, secreción ni mareos.");
slidePausa(4, S4, "ETAPA 1 · EN GRUPOS · 7 MIN", "Antes de ver los resultados", [
  "Entiende distinto según el día, mejor mirando los labios, peor con ruido. ¿Qué antecedentes perinatales pesan y por qué?",
  "«El examen de oído al nacer salió bueno.» ¿Por qué un tamizaje con emisiones no descarta nada aquí? ¿Qué debió hacerse?",
  "Planteen al menos tres causas de que una adolescente «oiga pero no entienda».",
  "¿Qué pruebas separan una causa coclear de una neural? Si el PEAT sale plano, ¿qué harían antes de informarlo?",
], "Esperado: fluctuación y dependencia visual sugieren falta de sincronía. Bilirrubina y prematurez = riesgo de neuropatía. Las emisiones pasan en la neuropatía: en RN de riesgo corresponde AABR. Hipótesis: coclear, atencional, central, neuropatía auditiva. Antes de informar un PEAT plano: polaridades separadas y tubo pinzado.");
{
  const s = nueva("CONTENIDO", S4);
  cabecera(s, CASOS[4].tag + " · RESULTADOS", "Audiometría y logoaudiometría", CASOS[4].col);
  fig(s, "cap13_neuropatia_audiosupra.png", M, Y0, 7.6, 4.0, "Audiograma, logoaudiometría y supraliminares de Esther");
  const x2 = M + 7.9, w2 = W - M - x2;
  fig(s, "cap13_neuropatia_logoaudiometria.png", x2, Y0, w2, 3.1, "Curvas de logoaudiometría de Esther que caen a intensidad alta");
  s.addText(puntos([["Pérdida leve a moderada, ", "casi plana (OD 25-35 dB; OI 35-45), sin componente conductivo."],
    ["Discriminación: ", "48 % OD (60 dB) y 28 % OI (70 dB); a 100 dB cae a 17 % y 7 %."]]),
    { x: M, y: Y0 + 4.1, w: CW, h: 1.1, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Con 25 a 40 dB de pérdida la discriminación debería ser mucho mejor. Además la curva cae al subir la intensidad (roll-over): subir el volumen no ayuda. SISI 10 %, Carhart 30 dB en 2 y 4 kHz, Metz ausente bilateral.");
}
{
  const s = nueva("CONTENIDO", S4);
  cabecera(s, CASOS[4].tag + " · RESULTADOS", "Reflejos ausentes, emisiones presentes", CASOS[4].col);
  const fw = (CW - 0.4) / 2;
  fig(s, "cap13_neuropatia_impedancia.png", M, Y0, fw, 2.75, "Timpanogramas normales y reflejos ausentes de Esther");
  fig(s, "cap13_neuropatia_teoae.png", M + fw + 0.4, Y0, fw, 2.3, "Emisiones otoacústicas transitorias presentes");
  fig(s, "cap13_neuropatia_dpoae.png", M + fw + 0.4, Y0 + 2.5, fw, 2.3, "Productos de distorsión presentes");
  s.addText(puntos([["Reflejo ausente ", "en los cuatro arreglos, con oído medio normal: el arco no recibe una señal sincrónica."],
    ["TEOAE: ", "5 de 5 bandas; reproducibilidad 89 % (OD) y 93 % (OI)."],
    ["DPOAE: ", "presentes en las 7 frecuencias, en los dos oídos."]]),
    { x: M, y: Y0 + 2.95, w: fw, h: 2.2, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Las células ciliadas externas funcionan, aunque el audiograma marque 25 a 45 dB.");
}
{
  const s = nueva("CONTENIDO", S4);
  cabecera(s, CASOS[4].tag + " · RESULTADOS", "PEAT con polaridad alternada: plano", CASOS[4].col);
  fig(s, "cap13_neuropatia_abr.png", M, Y0, 8.4, 4.5, "PEAT de Esther sin ondas a 80, 60 y 40 dB nHL en los dos oídos");
  const x2 = M + 8.7, w2 = W - M - x2;
  tarjeta(s, x2, Y0, w2, 3.4);
  s.addText([{ text: "¿Lo informamos así?", options: { bold: true, fontSize: 20, color: C.text2, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Sin ondas a 80, 60 y 40 dB nHL en ninguno de los dos oídos. No es un umbral: con un audiograma de 25 a 45 dB, el PEAT no calza." }],
    { x: x2 + 0.25, y: Y0 + 0.2, w: w2 - 0.5, h: 3.0, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Antes de mostrar la siguiente, preguntar qué harían. Respuesta: separar las polaridades (rarefacción y condensación) a alta intensidad.");
}
{
  const s = nueva("CONTENIDO", S4);
  cabecera(s, CASOS[4].tag + " · RESULTADOS", "Rarefacción y condensación: algo se invierte", CASOS[4].col);
  s.addText("Rarefacción · 90 dB nHL", { x: M, y: Y0, w: 8.4, h: 0.35, fontSize: 15, bold: true, color: C.text2, margin: 0, isTextBox: true });
  fig(s, "cap13_neuropatia_abr_2.png", M, Y0 + 0.35, 8.4, 1.95, "PEAT en rarefacción con deflexión inicial hacia abajo");
  s.addText("Condensación · 90 dB nHL", { x: M, y: Y0 + 2.45, w: 8.4, h: 0.35, fontSize: 15, bold: true, color: C.text2, margin: 0, isTextBox: true });
  fig(s, "cap13_neuropatia_abr_3.png", M, Y0 + 2.8, 8.4, 1.95, "PEAT en condensación con la deflexión invertida");
  const x2 = M + 8.7, w2 = W - M - x2;
  tarjeta(s, x2, Y0, w2, YMAX - Y0);
  s.addText(puntos([["Primer milisegundo: ", "deflexión hacia abajo en rarefacción y hacia arriba en condensación."],
    ["Es la microfónica coclear: ", "sigue la forma del estímulo. La alternada la cancelaba."],
    ["Detrás no hay ondas neurales.", ""],
    ["Para descartar artefacto: ", "repetir con el tubo pinzado."]]),
    { x: x2 + 0.25, y: Y0 + 0.2, w: w2 - 0.5, h: YMAX - Y0 - 0.4, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Con el tubo pinzado, la microfónica desaparece (no llega sonido al oído); un artefacto electromagnético del transductor persiste.");
}
slideFigura(4, S4, "Potencial cortical: el sonido llega a la corteza", "cap13_neuropatia_cortical.png",
  "Potencial cortical P1-N1-P2 de Esther en los dos oídos", [
    ["OD: ", "P1 87, N1 128, P2 198 ms; N1-P2 de 7 y 8 µV."],
    ["OI: ", "P1 89, N1 120, P2 216 ms; N1-P2 de 5 y 5 µV."],
    ["Referencia orientativa: ", "P1 ≈ 67 ms a los 15 años; N1 100-130; P2 200-250 ms."],
    ["P1 tardía: ", "el tono está solo 20 dB sobre su umbral; no se lee como retardo de maduración."],
  ], "Tone burst de 1.000 Hz a 70 dB nHL. El cortical dice que hay vía por donde entrenar; no mide lo que entiende: la discriminación dice que entiende solo en parte. En niños con neuropatía, corticales presentes se asocian a mejor percepción del habla (Rance y cols., 2002).", 8.0);
slidePausa(4, S4, "ETAPA 2 · EN GRUPOS · 10 MIN", "Interpreten los resultados", [
  "¿Calza 48 % y 28 % con un umbral de 25 a 45 dB? ¿Qué significa que la curva caiga a 100 dB?",
  "Con oído medio normal, ¿qué dice un reflejo ausente en los cuatro arreglos? ¿Y unas emisiones presentes?",
  "¿Qué es la deflexión que se invierte? ¿Por qué la alternada la borra? ¿Cómo descartan artefacto?",
  "¿Puede este PEAT estimar el umbral? ¿Qué pasaría si se informara «hipoacusia profunda»?",
  "¿Qué dice y qué no dice el potencial cortical? Redacten conclusión y recomendación.",
  "La mamá dice que «oye cuando quiere». ¿Cómo le explican el resultado?",
], "Respuestas en la guía docente, caso 4. Errores esperables: llamarla sorda por el PEAT plano; ofrecer audífono sin ver la discriminación; quedarse en «es distraída».");
slideCierre(4, S4, "Patrón de neuropatía auditiva bilateral", [
  ["Cóclea sí, nervio no", "Emisiones y microfónica presentes; PEAT sin ondas neurales; reflejos ausentes; discriminación desproporcionada."],
  ["No es sordera", "En este patrón el PEAT no estima el umbral. El cortical presente dice que hay vía por donde entrenar."],
  ["Lo que sigue", "Tubo pinzado; derivar a ORL y rehabilitación. No fijar el audífono con el audiograma: su beneficio suele ser menor."],
], "Beneficio del audífono variable: ~15 % refiere algún beneficio (Berlin y cols., 2010); BSA 2019. Apoyos visuales y sistemas FM se deciden con el equipo. Un RN con factores de riesgo necesita AABR, no solo emisiones.");

// =====================================================================
// Plenario
// =====================================================================
const S5 = "Plenario";
slidePausa(null, S5, "PLENARIO · 15 MIN", "Integrar los cuatro casos", [
  "Verónica y Álvaro tuvieron una prueba con fármaco. ¿Qué pregunta responde cada una? ¿Por qué en ella no cambia nada y en él casi todo?",
  "Lourdes y Esther dicen lo mismo: «oye pero no entiende». ¿Qué examen las separa?",
  "En cada caso hay una cifra resumen que engaña. ¿Cuál es y cómo engaña?",
  "En ningún informe se escribió un diagnóstico. ¿Por qué? ¿Qué gana el paciente?",
  "Elijan un caso: una acción de prevención primaria, una secundaria y una cuaternaria.",
], "Cifras que engañan: Verónica, VEF1 y razón normales con una vía aérea alta estrecha; Álvaro, el reposo si llega con el spray puesto; Lourdes, PEAT sin ondas por la pérdida; Esther, PEAT plano que parece sordera y audiograma leve que parece «audífono y listo».");
{
  const s = nueva("CONTENIDO", S5);
  cabecera(s, "PLENARIO", "Lourdes y Esther, lado a lado");
  s.addTable(tabla([["", "Lourdes, 52 años", "Esther, 15 años"],
    ["Lado", "Unilateral (OD)", "Bilateral"],
    ["Umbral", "Severo en agudos", "Leve a moderado, plano"],
    ["Discriminación", "20 % en el OD", "48 % y 28 %, con caída a 100 dB"],
    ["Reflejos", "Patrón diagonal (aferente OD)", "Ausentes en los cuatro arreglos"],
    ["Emisiones y microfónica", "No se estudiaron en el caso", "Presentes"],
    ["PEAT", "OD: III y V solo a 90-100 dB; OI normal", "Sin ondas neurales en los dos"],
    ["VEMP o cortical", "VEMP OD disminuido (63 %)", "Cortical presente"],
    ["Lo que sigue", "RM de CAI con gadolinio", "ORL y equipo de rehabilitación"]], {}),
    Object.assign({ x: M, y: Y0, w: CW, colW: [3.0, (CW - 3.0) / 2, (CW - 3.0) / 2], rowH: 0.52 }, TB, { fontSize: 16 }));
  s.addNotes("Mostrar después de que los grupos armen su propia tabla.");
}
{
  const s = nueva("FICHA", S5);
  s.addText("PARA LLEVARSE", { x: M + 0.2, y: 0.7, w: 10, h: 0.4, fontSize: 15, bold: true, color: "F2C46D", charSpacing: 2, margin: 0, isTextBox: true });
  s.addText("Cinco ideas del taller", { x: M + 0.2, y: 1.15, w: 11, h: 0.8, fontSize: 36, bold: true, fontFace: "Cambria", color: C.background1, margin: 0, isTextBox: true });
  const ideas = [
    ["1", "Una cifra resumen (VEF1 normal, total nasal, PEAT plano, umbral) no reemplaza mirar la curva y cada parte del examen."],
    ["2", "Las pruebas con fármaco (broncodilatador, vasoconstrictor) separan lo reversible de lo fijo; no dicen la causa."],
    ["3", "Con pérdida severa el PEAT pierde poder: pesan la discriminación, los reflejos y el VEMP."],
    ["4", "Emisiones presentes y PEAT ausente: neuropatía. El PEAT no estima umbral; separar polaridades antes de informar."],
    ["5", "El informe describe un patrón. Diagnóstico y tratamiento son del médico."],
  ];
  ideas.forEach(([n, t], i) => {
    const y = 2.2 + i * 0.93;
    s.addShape(pres.shapes.OVAL, { x: M + 0.2, y, w: 0.62, h: 0.62, fill: { color: "F2C46D" }, line: { color: "F2C46D" } });
    s.addText(n, { x: M + 0.2, y, w: 0.62, h: 0.62, fontSize: 20, bold: true, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(t, { x: M + 1.1, y: y - 0.05, w: 10.8, h: 0.75, fontSize: 18, color: C.background1, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addNotes("Cerrar con estas cinco ideas. Recoger los informes grupales si se van a evaluar.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ok", OUT);
})();
