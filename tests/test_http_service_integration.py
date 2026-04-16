import importlib.util
import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
import os


HAS_FLASK = importlib.util.find_spec('flask') is not None


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('127.0.0.1', 0))
        return int(sock.getsockname()[1])


@pytest.mark.skipif(not HAS_FLASK, reason='Flask not installed')
def test_start_http_service_script_serves_verify_endpoint():
    port = _free_port()
    env = dict(os.environ)
    env['PYTHONPATH'] = 'src'
    process = subprocess.Popen(
        [
            sys.executable,
            'scripts/start_http_service.py',
            '--policy-path',
            'data/policies.json',
            '--revocation-path',
            'data/revocations.json',
            '--host',
            '127.0.0.1',
            '--port',
            str(port),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    try:
        health_url = f'http://127.0.0.1:{port}/health'
        verify_url = f'http://127.0.0.1:{port}/trqp/verify'
        for _ in range(30):
            try:
                with urllib.request.urlopen(health_url, timeout=1) as resp:
                    if resp.status == 200:
                        break
            except Exception:
                time.sleep(0.2)
        payload = json.loads(Path('examples/verification_request.json').read_text(encoding='utf-8'))
        body = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(verify_url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        assert result['trust_outcome'] in {'trusted', 'trusted_cached'}
        assert result['verification_mode'] == 'cached_online'
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
