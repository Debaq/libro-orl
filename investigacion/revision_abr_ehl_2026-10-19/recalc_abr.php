<?php
// Recalcula el ABR (umbral y umbral por estímulo, aéreo y óseo) de cada caso
// con CaseProfile::project(), igual que CaseForm al guardar. Uso:
//   php recalc_abr.php <labsim_backend> <salida.json> <caso.json|casos_demo.json>...
$backend = $argv[1];
require_once $backend . '/src/CaseProfile.php';
require_once $backend . '/src/CaseForm.php';
$out = [];
foreach (array_slice($argv, 3) as $ruta) {
    $j = json_decode(file_get_contents($ruta), true);
    $lista = isset($j['data']) ? ['' => $j] : $j;           // generado o casos_demo
    foreach ($lista as $clave => $caso) {
        $d = $caso['data'] ?? $caso;
        $perfil = CaseProfile::normalize($d);
        $edad = (int) ($d['edad'] ?? 0);
        $horas = ($edad === 0 && isset($d['edad_horas']) && $d['edad_horas'] !== '' && $d['edad_horas'] !== null)
            ? (float) $d['edad_horas'] : null;
        $meses = $horas !== null ? $horas / 720.0 : $edad * 12.0;
        $z = function ($v) { return is_string($v) && $v !== '' ? $v : 'A'; };
        $nac = is_array($d['nacimiento'] ?? null) ? $d['nacimiento'] : [];
        $p = CaseProfile::project($d['Aerea'] ?? [], $d['Osea'] ?? [], $perfil,
            ['OD' => $z($d['Z_OD'] ?? 'A'), 'OI' => $z($d['Z_OI'] ?? 'A')], $horas, $meses, $nac);
        $r = [];
        foreach (['OD', 'OI'] as $l) {
            $r[$l] = ['umbral' => $p['abr'][$l]['umbral'],
                      'umbral_por_estimulo' => $p['abr'][$l]['umbral_por_estimulo'],
                      'umbral_por_estimulo_oseo' => $p['abr'][$l]['umbral_por_estimulo_oseo']];
        }
        $out[$ruta . ($clave === '' ? '' : '#' . $clave)] = ['meses' => $meses, 'abr' => $r];
    }
}
file_put_contents($argv[2], json_encode($out, JSON_PRETTY_PRINT));
echo count($out), " casos\n";
