import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate, Counter } from 'k6/metrics';

// ── Custom Metrics ──
const bookingCreationDuration = new Trend('booking_creation_duration');
const bookingFetchDuration = new Trend('booking_fetch_duration');
const errorRate = new Rate('custom_error_rate');
const successfulBookings = new Counter('successful_bookings');

// ── Configuration & Thresholds ──
export const options = {
  stages: [
    { duration: '10s', target: 5 },   // Ramp-up to 5 virtual users
    { duration: '30s', target: 10 },  // Steady state with 10 virtual users
    { duration: '10s', target: 0 },   // Ramp-down to 0 virtual users
  ],
  thresholds: {
    // Non-negotiable requirement: 95th percentile response time must be under 800ms
    http_req_duration: ['p(95)<800'],
    // HTTP failure rate should stay under 5%
    http_req_failed: ['rate<0.05'],
    custom_error_rate: ['rate<0.05'],
    booking_creation_duration: ['p(95)<800'],
    booking_fetch_duration: ['p(95)<800'],
  },
};

const BASE_URL = __ENV.API_BASE_URL || 'https://restful-booker.herokuapp.com';
const USERNAME = __ENV.API_USERNAME || 'admin';
const PASSWORD = __ENV.API_PASSWORD || 'password123';

// ── Global Setup: Authenticate once to obtain admin token ──
export function setup() {
  const authPayload = JSON.stringify({
    username: USERNAME,
    password: PASSWORD,
  });

  const authParams = {
    headers: { 'Content-Type': 'application/json' },
  };

  const authRes = http.post(`${BASE_URL}/auth`, authPayload, authParams);
  const isAuthOk = check(authRes, {
    'auth succeeded (200)': (r) => r.status === 200,
    'token received': (r) => r.json('token') !== undefined,
  });

  if (!isAuthOk) {
    console.error('Setup failed: Unable to obtain auth token');
  }

  return { token: authRes.json('token') };
}

// ── Main Virtual User Flow ──
export default function (data) {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  // 1. Create a Booking
  const createPayload = JSON.stringify({
    firstname: `K6User_${__VU}`,
    lastname: `Iter_${__ITER}`,
    totalprice: 150,
    depositpaid: true,
    bookingdates: {
      checkin: '2026-09-01',
      checkout: '2026-09-07',
    },
    additionalneeds: 'High-speed Wi-Fi',
  });

  const createRes = http.post(`${BASE_URL}/booking`, createPayload, { headers });
  bookingCreationDuration.add(createRes.timings.duration);

  const createSuccess = check(createRes, {
    'create booking status is 200': (r) => r.status === 200,
    'create returns valid bookingid': (r) => r.json('bookingid') > 0,
  });

  errorRate.add(!createSuccess);

  if (!createSuccess) {
    sleep(1);
    return;
  }

  const bookingId = createRes.json('bookingid');
  successfulBookings.add(1);

  // 2. Fetch the Created Booking
  const getRes = http.get(`${BASE_URL}/booking/${bookingId}`, {
    headers: { 'Accept': 'application/json' },
  });
  bookingFetchDuration.add(getRes.timings.duration);

  const getSuccess = check(getRes, {
    'get booking status is 200': (r) => r.status === 200,
    'get booking matches firstname': (r) => r.json('firstname') === `K6User_${__VU}`,
  });
  errorRate.add(!getSuccess);

  // 3. Update the Booking (PUT with Token)
  if (data && data.token) {
    const updatePayload = JSON.stringify({
      firstname: `K6User_${__VU}_Updated`,
      lastname: `Iter_${__ITER}`,
      totalprice: 220,
      depositpaid: false,
      bookingdates: {
        checkin: '2026-09-02',
        checkout: '2026-09-09',
      },
      additionalneeds: 'Late Checkout',
    });

    const authHeaders = {
      ...headers,
      'Cookie': `token=${data.token}`,
    };

    const updateRes = http.put(`${BASE_URL}/booking/${bookingId}`, updatePayload, {
      headers: authHeaders,
    });

    const updateSuccess = check(updateRes, {
      'update booking status is 200': (r) => r.status === 200,
    });
    errorRate.add(!updateSuccess);

    // 4. Delete the Booking (Clean-up)
    const deleteRes = http.del(`${BASE_URL}/booking/${bookingId}`, null, {
      headers: { 'Cookie': `token=${data.token}` },
    });

    const deleteSuccess = check(deleteRes, {
      'delete booking status is 201': (r) => r.status === 201,
    });
    errorRate.add(!deleteSuccess);
  }

  // Realistic think time between iterations
  sleep(1);
}
