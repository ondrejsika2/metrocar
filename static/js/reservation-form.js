/**
 * Created by PyCharm.
 * User: honca
 * Date: 25.6.11
 * Time: 10:28
 */

const TIME_DIVISION = 30;

//----------------------------------- pomocne staticke funkce ----------------------------------//

/**
 * Funkce vrati pole hodnot podle zadaneho rozsahu.
 * @param int start
 * @param int end
 * @param int step
 * @return Array
 */
function range(start, end, step) {
    if (typeof(step) == 'undefined') {
        step = 1;
    }
    var items = new Array();
    for (i = start; i < end; i = i + step) {
        items.push(i);
    }
    return items;
}

/**
 * Vrati objekt data podle zadaneho casoveho parametru
 * @param string datetime d.m.yyyy HH:MM
 */
function getDate(datetime) {
    var parts = datetime.split(' ');
    var date = parts[0].split('.');
    var time = parts[1].split(':');
    return new Date(date[2], date[1] - 1, date[0], time[0], time[1]);
}

/**
 * Povoli anebo zakaze odeslani rezervacniho formulare
 * @param value
 */
function disableReservationButton(button, value) {
    if (typeof(value) == 'undefined') {
        value = true;
    }
    button.attr('disabled', value)
          .removeClass(value ? 'grey' : 'green')
          .addClass(value ? 'green' : 'grey')
          .parents('span.button')
          .removeClass(value ? 'button-green' : 'button-grey')
          .addClass(value ? 'button-grey' : 'button-green');
}

//------------------------------- funkce obsluhujici rezervacni formular ------------------------------//

/**
 *
 * @param object $time html element s hodnotami casu
 * @param startTime vychozi cas, od ktereho se bude dale zvysovat
 */
function loadReservationTime($date, $time, startTime, selectedTime) {
    // pokud je datum prazdne, nastavime na dnesni den
    if ($date.val().length == 0) {
        var now = new Date();
        $date.val(now.format('d.m.yyyy'));
    }
    // pokud neni zadan zacatek casu, nastavime na zacatek dne
    if (typeof(startTime) == 'undefined') {
        startTime = '00:00';
    }
    // pokud neni zadan vybrany cas, nastavime na zacatek na prvni hodnotu
    if (typeof(selectedTime) == 'undefined') {
        selectedTime = startTime;
    }
    $time.html(''); // vynulovani hodnot

    var dateValue       = $date.val();
    var dateValues      = dateValue.split('.');
    var startTimeValues = startTime.split(':');
    var startHour       = parseInt(startTimeValues[0], 10);
    var startMinute     = parseInt(startTimeValues[1], 10);
    var value           = '';
    var date            = getDate(dateValue + ' ' + startTime);
    var timeFormat      = '';

    var hours = range(startHour, 24, 1);
    for (var h in hours) {
        var hour = hours[h];
        var minutes = range((hour > startHour ? 0 : startMinute), 60, 15);
        for (var m in minutes) {
            var minute = minutes[m];
            date.setHours(hour);
            date.setMinutes(minute);
            timeFormat = date.format('HH:MM');
            var option = $('<option value="' + timeFormat + '">' + timeFormat + '</option>');
            if (timeFormat == selectedTime) {
                option.attr('selected', 'selected');
            }
            $time.append(option);
        }
    }
}

$(function() {
    var $reservedStartDate = $('#id_0-reserved_from_0');
    var $reservedStartTime = $('#id_0-reserved_from_1');
    var $reservedEndDate = $('#id_0-reserved_until_0');
    var $reservedEndTime = $('#id_0-reserved_until_1');

    var defaultStartDate = $reservedStartDate.val();
    var defaultStartTime = $reservedStartTime.find('option:selected').text();
    var defaultEndDate = $reservedEndDate.val();
    var defaultEndTime = $reservedEndTime.find('option:selected').text();

    /**
     * Nahraje vsechna vozidla, ktera jsou ve vybranem case dostupna
     */
    var loadAvailableCars = function() {
        var startDate = $reservedStartDate.val();
        var startTime = $reservedStartTime.val();
        var endDate = $reservedEndDate.val();
        var endTime = $reservedEndTime.val();

        $.ajax({
            type: "GET",
            dataType: 'json',
            url: "/automobily/load_car_list/" + startDate + "/" + startTime + "/" + endDate + "/" + endTime + "/",
            success: function(data) {
                disableReservationButton($('button'), data.count == 0);
                $('#id_0-car_id').html(data.data);
            }
        });
    }

    var changeReservationStartDate = function(event) {
        // start
        var currentStartDateText = $(this).val();
        var currentStartTimeText = $reservedStartTime.find('option:selected').text();
        var currentStartDate = getDate(currentStartDateText + ' ' + currentStartTimeText);

        // end
        var currentEndDateText = $reservedEndDate.val();
        var currentEndTimeText = $reservedEndTime.find('option:selected').text();
        var currentEndDate   = getDate(currentEndDateText + ' ' + currentEndTimeText);

        if (currentStartDate != 'Invalid Date') {
            var startTime = '00:00';
            // pokud je datum nastaveno na vychozi (dnesek), tak se nastavi i vychozi cas
            if (currentStartDateText == defaultStartDate) {
                startTime = defaultStartTime;
            }
            loadReservationTime($reservedStartDate, $reservedStartTime, startTime, currentStartTimeText);

            if (currentStartDate >= currentEndDate) {
                currentEndDateText = $reservedEndDate.val(currentStartDateText).val();
                var endTime = '00:00';
                if (currentEndDateText == defaultEndDate) {
                    endTime = defaultEndTime;
                }
                loadReservationTime($reservedEndDate, $reservedEndTime, endTime, currentEndTimeText);
            }
        }
        loadAvailableCars();
    }

    var changeReservationEndDate = function(event) {
        // start
        var currentStartDateText = $reservedStartDate.val();
        var currentStartTimeText = $reservedStartTime.find('option:selected').text();
        var currentStartDate = getDate(currentStartDateText + ' ' + currentStartTimeText);

        // end
        var currentEndDateText = $(this).val();
        var currentEndTimeText = $reservedEndTime.find('option:selected').text();
        var currentEndDate   = getDate(currentEndDateText + ' ' + currentEndTimeText);

        if (currentEndDate != 'Invalid Date') {
            var endTime = '00:00';
            // pokud je datum nastaveno na vychozi (dnesek), tak se nastavi i vychozi cas
            if (currentEndDateText == defaultEndDate) {
                endTime = defaultEndTime;
            }
            loadReservationTime($reservedEndDate, $reservedEndTime, endTime, currentEndTimeText);

            if (currentEndDate <= currentStartDate) {
                currentStartDateText = $reservedStartDate.val(currentEndDateText).val();
                var startTime = '00:00';
                if (currentStartDateText == defaultStartDate) {
                    startTime = defaultStartTime;
                }
                loadReservationTime($reservedStartDate, $reservedStartTime, startTime, currentStartTimeText);
            }
        }
        loadAvailableCars();
    }

    // zmena zacatku rezervace
    $reservedStartDate.change(changeReservationStartDate);
    $reservedStartDate.keyup(changeReservationStartDate);

    // zmena konce rezervace
    $reservedEndDate.change(changeReservationEndDate);
    $reservedEndDate.keyup(changeReservationEndDate);

    $reservedStartTime.change(loadAvailableCars);
    $reservedEndTime.change(loadAvailableCars);
});
