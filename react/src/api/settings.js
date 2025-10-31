import instance from './axios';

const DEFAULT_SETTINGS = { header_title: 'Авитолог' };

export async function getSettings() {
  try {
    const res = await instance.get('/api/settings', { params: { _ts: Date.now() } });
    const title = typeof res?.data?.header_title === 'string' && res.data.header_title.trim()
      ? res.data.header_title.trim()
      : DEFAULT_SETTINGS.header_title;
    return { header_title: title };
  } catch (e) {
    console.warn('Failed to fetch /api/settings, using fallback');
    return DEFAULT_SETTINGS;
  }
}
