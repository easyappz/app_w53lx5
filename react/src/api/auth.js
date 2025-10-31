import instance from './axios';

export async function register({ username, password }) {
  const res = await instance.post('/api/auth/register/', { username, password });
  return res.data; // { username, token }
}

export async function login({ username, password }) {
  const res = await instance.post('/api/auth/login/', { username, password });
  return res.data; // { username, token }
}

export async function me() {
  const res = await instance.get('/api/auth/me/');
  return res.data; // { username }
}
