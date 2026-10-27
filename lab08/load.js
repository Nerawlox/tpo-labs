import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    training: {executor:'constant-vus', vus:Number(__ENV.VUS || 10), duration:__ENV.DURATION || '30s', gracefulStop:'5s'},
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const response = http.get(`${__ENV.BASE_URL || 'http://127.0.0.1:8765'}/api/health`, {timeout:'5s'});
  check(response, {
    'status 200': r => r.status === 200,
    'valid body': r => {try {return r.json('status') === 'ok' && r.json('service') === 'training-api';} catch (_) {return false;}},
  });
  sleep(0.05);
}

export function handleSummary(data) {
  const m = data.metrics;
  const text = [
    `k6 / Local training API / ${__ENV.VUS} VUs / ${__ENV.DURATION}`,
    `Requests: ${m.http_reqs.values.count}`,
    `Requests per second: ${m.http_reqs.values.rate.toFixed(2)}`,
    `Average response (ms): ${m.http_req_duration.values.avg.toFixed(3)}`,
    `p95 response (ms): ${m.http_req_duration.values['p(95)'].toFixed(3)}`,
    `Error rate: ${(m.http_req_failed.values.rate*100).toFixed(3)}%`,
    `Checks passed: ${m.checks.values.passes}; failed: ${m.checks.values.fails}`,
    `Thresholds: error <1%, p95 <500ms, checks >99%`,
  ].join('\n') + '\n';
  return { stdout:text, [__ENV.OUTPUT || 'lab08/results/summary.json']:JSON.stringify(data,null,2) };
}
