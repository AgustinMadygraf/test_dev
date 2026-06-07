const { mapExpediente } = require('../test_helpers/mapExpediente');

test('mapExpediente prefers id_propietario and falls back to owner_id', () => {
  const api = { id: 1, numero: 'A1', extracto: 'X', owner_id: 'owner-123' };
  const vm = mapExpediente(api);
  expect(vm.id_propietario).toBe('owner-123');
  expect(vm.id).toBe(1);
});

test('mapExpediente uses id_propietario when present', () => {
  const api = { id: 2, numero: 'B2', extracto: 'Y', id_propietario: 'prop-999' };
  const vm = mapExpediente(api);
  expect(vm.id_propietario).toBe('prop-999');
});

test('mapExpediente fills descripcion with null when missing', () => {
  const api = { id: 3, numero: 'C3', extracto: 'Z' };
  const vm = mapExpediente(api);
  expect(vm.descripcion).toBeNull();
});
