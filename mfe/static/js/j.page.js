function markupDatepickers(rootNode)
{
        var node = $('<a href="#" class="button button-icon-solo j-datepicker-launcher ui-state-default ui-corner-all"><span class="ui-icon ui-icon-calendar">Vybrat</span></a>');

        /* add datepicker icon next to the input */
        rootNode.find(".datepicker")
                .after(node);

        rootNode.find('.j-datepicker-launcher').unbind('click').click(function () {
                $(this).prev('.datepicker')
                        .datepicker({
                                onClose: function (date) {
                                        $(this).datepicker('destroy');
                                }
                        })
                        .datepicker('show');

                return false;
        });

        node = $('<a href="#" class="button button-icon-left j-timepicker-launcher ui-state-default ui-corner-all"><span class="ui-icon ui-icon-clock"></span>Nyní</a>');
        /* add timepickers */
        rootNode.find(".timepicker")
                .after(node);

        rootNode.find('.j-timepicker-launcher').unbind('click').click(function () {
                var date      = new Date();
                var currHour  = date.getHours();
                var currMin   = date.getMinutes();
                var currSec       = date.getSeconds();

                var timeVal = currHour;
                timeVal    += ((currMin < 10) ? ":0" : ":") + currMin;
                timeVal    += ((currSec < 10) ? ":0" : ":") + currSec;

                $(this).prev('.timepicker').val(timeVal);

                return false;
        });
}

$(document).ready(function () {
	var popups = new Array();
	popups['#subsidiary-list'] = true;
	popups['#login-box'] = true;
	
	$('span.search input[type=text]').live('focus', function () {
		$(this).val('');
	});
	
	$('#j-open-subsidiary-selector').unbind('click').click(function () {
		$($(this).attr('href')).show();
		return false;
	});
	
	$('#j-open-login-box').unbind('click').click(function () {
		$('#login-box').show();
		return false;
	});
	
	$('#subsidiary-list')
		.mouseenter(function () { popups['#subsidiary-list'] = false; })
		.mouseleave(function () { popups['#subsidiary-list'] = true; });
	
	$('#login-box')
		.mouseenter(function () { popups['#login-box'] = false; })
		.mouseleave(function () { popups['#login-box'] = true; });
	
	$(document).mousedown(function () { 
		for (key in popups) {
			if (popups[key]) $(key).hide();
		}
	});
	
	 $.datepicker.setDefaults({
	         dateFormat: 'd.m.yy',
	         monthNames: ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'],
	         dayNames: ['Neděle', 'Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota'],
	         dayNamesMin: ['Ne', 'Po', 'Út', 'St', 'Čt', 'Pá', 'So'],
	         firstDay: 1,
	         nextText: 'Další',
	         prevText: 'Předchozí'
	 });
	
	markupDatepickers($(document));
});