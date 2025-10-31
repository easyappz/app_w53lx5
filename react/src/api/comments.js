import instance from './axios';

let loaded = false;
async function ensure() {
  if (loaded) return;
  try {
    await fetch('/api_schema.yaml', { cache: 'no-cache' });
  } catch (e) {
    console.warn('Could not verify api_schema.yaml for comments');
  } finally {
    loaded = true;
  }
}

export async function listByAd(adId) {
  await ensure();
  const res = await instance.get(`/api/ads/${adId}/comments`);
  return res.data;
}

export async function create(adId, text) {
  await ensure();
  const res = await instance.post(`/api/ads/${adId}/comments`, { text });
  return res.data;
}
