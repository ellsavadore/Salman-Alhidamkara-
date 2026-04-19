// Google Apps Script untuk QR Code Attendance System
// Cara penggunaan: Copy script ini ke Google Apps Script, lalu deploy sebagai Web App

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
      .setTitle('QR Code Attendance System')
      .setFaviconUrl('https://www.google.com/s2/favicons?domain=www.google.com');
}

function recordAttendance(employeeId, employeeName) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var timestamp = new Date();
  var date = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  var time = Utilities.formatDate(timestamp, Session.getScriptTimeZone(), 'HH:mm:ss');
  
  // Cek apakah sudah absen hari ini
  var lastRow = sheet.getLastRow();
  for (var i = 2; i <= lastRow; i++) {
    if (sheet.getRange(i, 2).getValue() === date && 
        sheet.getRange(i, 3).getValue() === employeeId) {
      return { success: false, message: 'Anda sudah absen hari ini' };
    }
  }
  
  // Tambah data absen
  sheet.appendRow([
    timestamp,
    date,
    time,
    employeeId,
    employeeName,
    'Hadir',
    'QR Code'
  ]);
  
  return { success: true, message: 'Absen berhasil dicatat' };
}

function getAllAttendance() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  return data;
}
