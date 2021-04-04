// カレンダーID（外部に漏れないよう注意！）
// "_gcalendar.gs"を同じ場所にコピーして"gcalendar.gs"にリネームしてから3行目を追記してください
var calId = "(ここにIDをペースト)"

function doGet(e) {
  start_date_year = e.parameter.year;
  start_date_month = e.parameter.month;
  start_date_day = e.parameter.day;
  payload = JSON.stringify(getWeeklyEvents(
    calId, start_date_year, start_date_month, start_date_day
  ));

  // ref.) https://qiita.com/tfuruya/items/3c306ee03d1ac290bcef
  ContentService.createTextOutput();
  var output = ContentService.createTextOutput();
  output.setMimeType(ContentService.MimeType.JSON);
  output.setContent(payload);

  return output;
}

// 1週間のイベントをカレンダーから取得
function getWeeklyEvents(calId, year, month, day) {
  var weeklyEvents = {};
  var cal = CalendarApp.getCalendarById(calId);
  var start_date = new Date(year, month, day);
  
  for(var elapsedDays=0; elapsedDays<7; elapsedDays++) {
    var events = cal.getEventsForDay(start_date);
    var n_event = events.length;  // イベント数

    // イベントなし -> 次の日へ
    if(n_event == 0) {
      start_date.setDate(start_date.getDate() + 1);
      continue;
    }

    weeklyEvents[elapsedDays] = {}
    for(var j=0; j<n_event; j++) {
      var startTime = dateToFormatString(events[j].getStartTime(), "%HH%:%mm%");  // 開始時間
      var endTime = dateToFormatString(events[j].getEndTime(), "%HH%:%mm%");      // 終了時間

      var eventTime = startTime + "~" + endTime;  // イベント時間: 開始時間~終了時間
      var eventTitle = events[j].getTitle();      // イベントタイトル
      
      // イベント時間: イベントタイトル
      weeklyEvents[elapsedDays][eventTime] = eventTitle;
    }
    
    start_date.setDate(start_date.getDate() + 1);
  }
  
  return weeklyEvents;
}
