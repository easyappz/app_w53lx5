import instance from './axios';

let schemaLoaded = false;
let schemaText = '';
let cachedSettings = null;

const DEFAULT_SETTINGS = { header_title: 'Авитолог' };

function hasSettingsPath(text) {
  if (!text) return false;
  return text.indexOf('/api/settings:') !== -1;
}

async function ensureSchemaLoaded() {
  if (schemaLoaded) return;
  try {
    if (typeof window !== 'undefined' && window.__API_SCHEMA_YAML__) {
      schemaText = String(window.__API_SCHEMA_YAML__ || '');
    } else {
      const resp = await fetch('/api_schema.yaml', { cache: 'no-cache' });
      schemaText = await resp.text();
      if (typeof window !== 'undefined') {
        window.__API_SCHEMA_YAML__ = schemaText;
      }
    }

    if (!hasSettingsPath(schemaText)) {
      console.warn('api_schema.yaml is missing expected path:', '/api/settings');
    }
  } catch (e) {
    console.error('Failed to load api_schema.yaml', e);
  } finally {
    schemaLoaded = true;
  }
}

export async function getSettings() {
  await ensureSchemaLoaded();

  if (!hasSettingsPath(schemaText)) {
    return DEFAULT_SETTINGS;
  }

  if (cachedSettings) return cachedSettings;

  try {
    const res = await instance.get('/api/settings');
    const title = res && res.data && typeof res.data.header_title === 'string' && res.data.header_title.trim()
      ? res.data.header_title.trim()
      : DEFAULT_SETTINGS.header_title;
    cachedSettings = { header_title: title };
    return cachedSettings;
  } catch (e) {
    console.warn('Failed to fetch /api/settings, using fallback');
    return DEFAULT_SETTINGS;
  }
}
