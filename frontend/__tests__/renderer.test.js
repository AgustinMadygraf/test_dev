const { createRowHTML } = require('../test_helpers/renderer');

test('createRowHTML includes owner when id_propietario present', () => {
  const exp = { id: 10, numero: 'N10', extracto: 'ext', id_propietario: 'u-1', descripcion: 'desc' };
  const html = createRowHTML(exp);
  expect(html).toContain('Owner: u-1');
  expect(html).toContain('N10');
});

test('createRowHTML uses N/A when owner missing', () => {
  const exp = { id: 11, numero: 'N11', extracto: 'ext2' };
  const html = createRowHTML(exp);
  expect(html).toContain('Owner: N/A');
});
