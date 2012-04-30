============
Car Unit API
============

Current API
===========
Is not very nice.

Proposal for the new car unit API.
==================================

Should follow the REST principles, since that is kind of the standard now and people that will be working on this project might already be familiar with it -- and if not, learning it will likely be beneficial to them.

Main features should be:
* simple
* easily debuggable


base url: https://autonapul.cz/carunit/v1/

GET reservations

	response: {



	}




POST status-update:

data::

	{

		auth_key: String

		datetime: yyyy-mm-dd hh:mm:ss.sss TZ ?

		coordinates: [lat: Number, lng: Number]

		status: 'DRIVING' | 'PARKED' | 'ENGINE_START' | 'ENGINE_OFF' | 'UNLOCKED' | 'LOCKED' | 'ALARM' | ...

		user_id: Number

		car_data {
			odometer, rpm, gear, gforce, consumption, errors, ???
		}
	}

	response:

		200 {
			status: 'Successfully saved'
		}

		400 {
			error: "Missing auth_key" | ...
		}
