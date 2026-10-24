from pathlib import Path
import subprocess
import tempfile

source = (Path(__file__).resolve().parents[1] / 'SOURCES/nginx.upgrade.sh').read_text()
failures = []
for case in ('invalid-config', 'missing-new-pid', 'signal-failed', 'successful-upgrade'):
    with tempfile.TemporaryDirectory(prefix='nginx-upgrade-guard-') as tmp:
        root = Path(tmp)
        (root / 'nginx.pid').write_text('12345\n')
        (root / 'nginx').write_text('#!/bin/bash\nexit "${CONFIG_RESULT:-0}"\n')
        (root / 'systemctl').write_text(f'#!/bin/bash\nprintf "PIDFile={root}/nginx.pid\\n"\n')
        (root / 'pkill').write_text('''#!/bin/bash
echo "${*: -1}" >> "$FIXTURE/actions"
if [ "${*: -1}" = USR2 ]; then
    [ "$TEST_CASE" != signal-failed ] || exit 1
    mv "$FIXTURE/nginx.pid" "$FIXTURE/nginx.pid.oldbin"
    if [ "$TEST_CASE" = successful-upgrade ]; then echo 23456 > "$FIXTURE/nginx.pid"; fi
fi
''')
        for name in ('nginx', 'systemctl', 'pkill'):
            (root / name).chmod(0o755)
        script = source.replace('/etc/sysconfig/nginx', str(root / 'sysconfig'))
        script = script.replace('nginx=/usr/sbin/nginx', f'nginx={root}/nginx')
        script = script.replace('/usr/bin/systemctl', str(root / 'systemctl'))
        (root / 'upgrade').write_text(script)
        env = dict(HOME=str(root), PATH=f'{root}:/usr/bin:/bin', FIXTURE=str(root), TEST_CASE=case,
                   SLEEPSEC='0', UPGRADEWAITLOOPS='1', CONFIG_RESULT='6' if case == 'invalid-config' else '0')
        result = subprocess.run(['bash', str(root / 'upgrade')], env=env, capture_output=True, text=True)
        actions = (root / 'actions').read_text().splitlines() if (root / 'actions').exists() else []
        expected_code = 6 if case == 'invalid-config' else 0 if case == 'successful-upgrade' else 1
        expected_actions = [] if case == 'invalid-config' else ['USR2', 'QUIT'] if case == 'successful-upgrade' else ['USR2']
        passed = result.returncode == expected_code and actions == expected_actions
        print(f'{case}: {"PASS" if passed else "FAIL"}, exit={result.returncode}, signals={actions}')
        if not passed:
            failures.append(case)
            print(result.stderr.strip())
if failures:
    raise SystemExit(1)
