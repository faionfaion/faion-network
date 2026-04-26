// lib/vapid.ts — canonical VAPID key converter
// Source of the most common "applicationServerKey is not valid" error.
// Test: assert that the output Uint8Array length is 65 for a P-256 public key.
export function urlBase64ToUint8Array(b64: string): Uint8Array {
  const pad = '='.repeat((4 - (b64.length % 4)) % 4);
  const norm = (b64 + pad).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(norm);
  const arr = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) {
    arr[i] = raw.charCodeAt(i);
  }
  return arr;
  // assert arr.length === 65 for a valid P-256 VAPID public key
}
