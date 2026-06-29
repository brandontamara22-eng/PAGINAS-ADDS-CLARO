const SHEET_ID = '1mErucwjxpCbX2kbv6nUFDeCKpJBoJuoOwXb2VeqtPYI';
const SHEET_NAME = 'Leads';

function doPost(e) {
  const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
  let sheet = spreadsheet.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);
  }

  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      'Fecha y hora',
      'Nombre y apellido',
      'Celular',
      'Distrito',
      'Plan seleccionado'
    ]);
    sheet.getRange(1, 1, 1, 5).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }

  sheet.appendRow([
    new Date(),
    e.parameter.name || '',
    e.parameter.phone || '',
    e.parameter.district || '',
    e.parameter.plan || 'Consulta general'
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return ContentService
    .createTextOutput('Conector de formularios activo')
    .setMimeType(ContentService.MimeType.TEXT);
}
