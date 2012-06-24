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
    var $car = $('#id_0-car_id');

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
        var selectedCarId = parseInt($car.find('option:selected').val());

        $.ajax({
            type: "GET",
            dataType: 'json',
            url: "/automobily/load_car_list/" + startDate + "/" + startTime + "/" + endDate + "/" + endTime + "/",
            success: function(data) {
                disableReservationButton($('button'), data.count == 0);
                $car.html(data.data);

                if (jQuery.inArray(selectedCarId, data.keys) > -1) {
                    $car.val(selectedCarId).attr('selected', 'selected');
                }
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

            if (currentStartDate >= currentEndDate) {
                currentEndDateText = $reservedEndDate.val(currentStartDateText).val();
                var endTime = '00:00';
                if (currentEndDateText == defaultEndDate) {
                    endTime = defaultEndTime;
                }
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

            if (currentEndDate <= currentStartDate) {
                currentStartDateText = $reservedStartDate.val(currentEndDateText).val();
                var startTime = '00:00';
                if (currentStartDateText == defaultStartDate) {
                    startTime = defaultStartTime;
                }
            }
        }
        loadAvailableCars();
    }

    $reservedStartDate.change(loadAvailableCars);
    $reservedStartDate.keyup(loadAvailableCars);

    $reservedEndDate.change(loadAvailableCars);
    $reservedEndDate.keyup(loadAvailableCars);

    $reservedStartTime.change(loadAvailableCars);
    $reservedEndTime.change(loadAvailableCars);

    /**
     *  V kroku pro shrnuti udaju rezervace umoznuje prepocitavat cenu
     *  podle zadaneho poctu kilometru. Vysledna cena je jen odhad te konecne.
     */

    var $reservationDistance = $('#reservation-distance');
    function recountReservationPriceEstimation() {
        var distance = $(this).val();

        // jednoducha kontrola proti nesmyslnym datum
        if (!$.isNumeric(distance) || distance > 1000000) {
            return;
        }

        var $priceByDistance = $('table.reservation-summary tbody tr.price-by-distance td');
        var $totalPriceEstimation = $('table.reservation-summary tbody tr.total-price td strong');
        var car_id = $('#id_0-car_id').val();
        var reserved_from_date = $('#id_0-reserved_from_0').val();
        var reserved_from_time = $('#id_0-reserved_from_1').val();
        var reserved_until_date = $('#id_0-reserved_until_0').val();
        var reserved_until_time = $('#id_0-reserved_until_1').val();

        $.ajax({
            type: "GET",
            data: {
                'distance': distance,
                'car_id': car_id,
                'reserved_from_date': reserved_from_date,
                'reserved_from_time': reserved_from_time,
                'reserved_until_date': reserved_until_date,
                'reserved_until_time': reserved_until_time
            },
            dataType: 'json',
            url: "/rezervace/recount_price_estimation/",
            success: function(data) {
                if (data) {
                    var $warningMsgRow = $('table.reservation-summary tbody tr.warning-msg td');
                    $priceByDistance.html(data['price_by_distance'] + ' Kč');
                    $totalPriceEstimation.html(data['total_price_estimation'] + ' Kč');
                    if (data['want_of_money']) {
                        var $warningMsg = $('<span class="info">' + data['warning_msg'] + '</div>');
                        $warningMsgRow.html($warningMsg);
                    } else {
                        $warningMsgRow.html('');
                    }
                }
            }
        });
    }

    $reservationDistance.on({
        'change': recountReservationPriceEstimation,
        'keyup': recountReservationPriceEstimation
    });
});