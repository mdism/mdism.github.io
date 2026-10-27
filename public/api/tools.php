<?php
/*
 * Lists the tools deployed on this subdomain, so the landing page never needs editing.
 * Every folder next to this site's root that has a tool.json is a tool. Read-only, no input, nothing stored.
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=300');
header('X-Content-Type-Options: nosniff');

$root  = dirname(__DIR__);
$tools = [];
foreach (glob($root . '/*/tool.json') ?: [] as $file) {
    $folder = basename(dirname($file));
    if (!preg_match('/^[a-z0-9-]+$/', $folder)) continue;           // only plain folder names
    $t = json_decode((string) file_get_contents($file, false, null, 0, 4096), true);
    if (!is_array($t) || empty($t['name'])) continue;
    $tools[] = [
        'name'   => mb_substr((string) $t['name'], 0, 60),
        'icon'   => mb_substr((string) ($t['icon'] ?? '•'), 0, 3),
        'desc'   => mb_substr((string) ($t['desc'] ?? ''), 0, 200),
        'url'    => '/' . $folder . '/',
        'status' => ($t['status'] ?? 'live') === 'soon' ? 'soon' : 'live',
        'order'  => (int) ($t['order'] ?? 100),
    ];
}
usort($tools, fn($a, $b) => [$a['order'], $a['name']] <=> [$b['order'], $b['name']]);
echo json_encode(array_map(fn($t) => array_diff_key($t, ['order' => 1]), $tools), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
