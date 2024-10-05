function updateCalendarEvents() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();
  var defaultCalendar = CalendarApp.getDefaultCalendar();
  var now = new Date();
  var endDate = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  var defaultEvents = defaultCalendar.getEvents(now, endDate).map(e => ({event: e, calendarName: 'Default'}));
  sheet.appendRow(['Event', 'Start', 'End', 'Description', 'Calendar', 'All-Day']);
  var eventRows = [];
  defaultEvents.forEach(eventObj => {
    var event = eventObj.event;
    var startTime = event.getStartTime();
    var endTime = event.getEndTime();
    var isAllDay = event.isAllDayEvent();
    if (endTime >= now || isAllDay) {
      eventRows.push([
        event.getTitle(),
        formatDateTime(startTime, isAllDay),
        formatDateTime(endTime, isAllDay),
        event.getDescription(),
        eventObj.calendarName,
        isAllDay ? 'Yes' : 'No'
      ]);
    }
  });
  eventRows.sort((a, b) => {
    if (a[5] === 'Yes' && b[5] === 'No') return -1;
    if (a[5] === 'No' && b[5] === 'Yes') return 1;
    return new Date(a[1].split(', ')[1]) - new Date(b[1].split(', ')[1]);
  });
  if (eventRows.length > 0) {
    sheet.getRange(2, 1, eventRows.length, 6).setValues(eventRows);
  }
  sheet.getRange(1, 1, 1, 6).setFontWeight('bold');
}

function formatDateTime(date, isAllDay) {
  var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var dayOfWeek = daysOfWeek[date.getDay()];
  var month = date.getMonth() + 1;
  var day = date.getDate();
  var year = date.getFullYear();
  if (isAllDay) {
    return `${dayOfWeek}, ${month}/${day}/${year}`;
  } else {
    var hours = date.getHours().toString().padStart(2, '0');
    var minutes = date.getMinutes().toString().padStart(2, '0');
    var seconds = date.getSeconds().toString().padStart(2, '0');
    return `${dayOfWeek}, ${month}/${day}/${year} ${hours}:${minutes}:${seconds}`;
  }
}
