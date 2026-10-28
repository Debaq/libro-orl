#!/usr/bin/env python3
"""Capturas del audiómetro de LabSim para las H (se corre aparte, no en el armado):

    labsim-audiometro-tono.png         H3: tono por el canal 1, ruido de banda estrecha por el 2
    labsim-audiometro-habla.png        H5: habla por el canal 1, ruido de habla por el 2
    labsim-audiometro-campo-libre.png  H8: el canal 1 en campo libre, con FM
    labsim-audiometro-vigilancia.png   H24: solo el canal 1, tono por vía aérea

Usa el script de capturas del manual de LabSim (docs/manual/capturas/
capturar_app.py) sin tocarlo: abre la app real sin pantalla, con un paciente
de práctica y sin red, y deja el audiómetro como lo dejaría el alumno, con
clics en los botones. Imprime, para cada captura, dónde queda cada control en
% del ancho y del alto: de ahí salen los globos del .md (él, 2026-10-28: el
audiómetro de LabSim cambió de estilo y la captura de H5 no estaba en Habla).

    micromamba run -n labsim python material/ilustraciones/hacer_capturas_audiometro.py
"""
import json
import os
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
LABSIM = pathlib.Path(os.environ.get('LABSIM', AQUI.parents[2] / 'LabSim'))
sys.path.insert(0, str(LABSIM / 'docs' / 'manual' / 'capturas'))
import capturar_app as C  # noqa: E402  (deja la app lista, sin red)

C.SALIDA = AQUI   # lo que el script de LabSim guarde, aquí y no en su repo


def guardar(widget, nombre):
    C.procesar()
    widget.grab().save(str(AQUI / f'{nombre}.png'))


CONTROLES = ['lbl_int_ch0', 'lbl_trans_ch0', 'lbl_output_ch0', 'lbl_int_ch1', 'lbl_prueba', 'lbl_response',
             'btn_output_der_ch0', 'btn_output_sim_ch0', 'btn_stim_tone_ch0', 'btn_stim_speech_ch0',
             'btn_stim_wn_ch0', 'btn_trans_aer_ch0', 'btn_trans_cl_ch0', 'btn_stim_sn_ch1', 'btn_stim_nbn_ch1',
             'btn_alt_frec', 'btn_freq_minus', 'btn_step_ch1', 'btn_ext_range', 'btn_correcta', 'btn_talkback',
             'btn_puls_ch0', 'btn_rever_ch0', 'btn_stim_ch0', 'btn_rever_ch1', 'dial_ch0']


def clic(a, *nombres):
    for n in nombres:
        getattr(a, n).click()
    C.procesar()


def donde(fa, a):
    """{control: [x0, y0, x1, y1]} en % de la captura."""
    W, H = fa.width(), fa.height()
    out = {}
    for n in CONTROLES:
        wd = getattr(a, n, None)
        if wd is None or not wd.isVisible():
            continue
        x, y, w, h = C.rect_de(fa, wd)
        out[n] = [round(100 * x / W, 1), round(100 * y / H, 1), round(100 * (x + w) / W, 1),
                  round(100 * (y + h) / H, 1)]
    return out


def sacar(nombre, armar):
    w, frame, ag = C.atendiendo('38')
    frame.hide()
    C.ir_a_box(w, 'Box Audiología')
    fa = C.abrir(w, 'A')
    armar(fa.obj)
    C.procesar()
    guardar(fa, nombre)
    print(nombre, json.dumps(donde(fa, fa.obj)), file=C._OUT)
    w.close()


def tono(a):
    # canal 1: tono a 40 dB HL al OD por fonos; canal 2: NBN a 60 dB al OI (el enmascarante)
    clic(a, 'btn_output_der_ch0', 'btn_stim_tone_ch0', 'btn_trans_aer_ch0',
         'btn_output_izq_ch1', 'btn_stim_nbn_ch1', 'btn_trans_aer_ch1')
    a.lbl_int_ch0.setText('40 dB HL')
    a.lbl_int_ch1.setText('60 dB HL')
    a.response.upHand()


def habla(a):
    # canal 1: habla a 50 dB HL al OD; canal 2: ruido de habla a 30 dB al OI
    clic(a, 'btn_output_der_ch0', 'btn_trans_aer_ch0', 'btn_stim_speech_ch0',
         'btn_output_izq_ch1', 'btn_trans_aer_ch1', 'btn_stim_sn_ch1')
    a.lbl_int_ch0.setText('50 dB HL')
    a.lbl_int_ch1.setText('30 dB HL')


def campo_libre(a):
    # canal 1 por el parlante derecho, con tono modulado
    clic(a, 'btn_trans_cl_ch0', 'btn_output_der_ch0', 'btn_stim_fm_ch0')
    a.lbl_int_ch0.setText('40 dB HL')


def vigilancia(a):
    # solo el canal 1: tono por fonos al OD
    clic(a, 'btn_output_der_ch0', 'btn_stim_tone_ch0', 'btn_trans_aer_ch0')
    a.lbl_int_ch0.setText('25 dB HL')


if __name__ == '__main__':
    try:
        for n, f in (('labsim-audiometro-tono', tono), ('labsim-audiometro-habla', habla),
                     ('labsim-audiometro-campo-libre', campo_libre), ('labsim-audiometro-vigilancia', vigilancia)):
            sacar(n, f)
    finally:
        C.registro.marcar_salida()
