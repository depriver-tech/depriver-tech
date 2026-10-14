const enc = new TextEncoder();
const base64 = bytes => btoa(String.fromCharCode(...bytes));
const bytes = text => Uint8Array.from(atob(text), c => c.charCodeAt(0));
async function key(env) {
  if (!env.SOCIAL_TOKEN_KEY) throw new Error('Token encryption is not configured.');
  const raw = bytes(env.SOCIAL_TOKEN_KEY);
  if (raw.length !== 32) throw new Error('Token encryption requires a 32-byte key.');
  return crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['encrypt','decrypt']);
}
export async function seal(value, env, platform) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = await crypto.subtle.encrypt({ name:'AES-GCM', iv, additionalData:enc.encode(platform) }, await key(env), enc.encode(value));
  return `${base64(iv)}.${base64(new Uint8Array(ciphertext))}`;
}
export async function unseal(value, env, platform) {
  const [iv, ciphertext] = value.split('.');
  const result = await crypto.subtle.decrypt({ name:'AES-GCM', iv:bytes(iv), additionalData:enc.encode(platform) }, await key(env), bytes(ciphertext));
  return new TextDecoder().decode(result);
}
