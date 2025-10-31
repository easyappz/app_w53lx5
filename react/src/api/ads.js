import instance from './axios';

let schemaLoaded = false;
let schemaText = '';

async function ensureSchemaLoaded() {
  if (schemaLoaded) return;
  try {
    const resp = await fetch('/api_schema.yaml', { cache: 'no-cache' });
    schemaText = await resp.text();
    // Basic verification that required paths exist
    const required = ['/api/ads:', '/api/ads/resolve:', '/api/ads/{id}:'];
    for (const p of required) {
      if (!schemaText.includes(p)) {
        console.warn('api_schema.yaml is missing expected path:', p);
      }
    }
    // Expose to window for debugging
    if (typeof window !== 'undefined') {
      window.__API_SCHEMA_YAML__ = schemaText;
    }
  } catch (e) {
    console.error('Failed to load api_schema.yaml', e);
  } finally {
    schemaLoaded = true;
  }
}

export async function listAds({ sort = 'popular', category = '', limit = 20, offset = 0 } = {}) {
  await ensureSchemaLoaded();
  const params = { sort, limit, offset };
  if (category && category.trim()) params.category = category.trim();
  const res = await instance.get('/api/ads', { params });
  return res.data;
}

export async function resolveAd(url) {
  await ensureSchemaLoaded();
  const res = await instance.post('/api/ads/resolve', { url });
  return res.data;
}

export async function getAd(id) {
  await ensureSchemaLoaded();
  const res = await instance.get(`/api/ads/${id}`);
  return res.data;
}
