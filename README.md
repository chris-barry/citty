# ciTTY

A status screen to help start your day.
Right now this only shows the weather and public transit times ([GTFS][gtfs] format).

I was inspired by [HackLab][hacklab]'s slick status screen, but didn't want to have a touch screen.
So I made my own that works in a TTY.

I have this running in my living room, on a [Raspberry Pi][pi] attached to a [VT220][vt220].

This requires Python 3 and has no dependencies.
This does however require a GTFS file in the `gtfs/` folder.
For copyright reasons I can't distribute mine.

[gtfs]: https://developers.google.com/transit/gtfs/
[hacklab]: https://hacklab.to/
[pi]: https://en.wikipedia.org/wiki/Raspberry_Pi
[vt220]: https://en.wikipedia.org/wiki/VT220

## Screenshot

	┌───────────────────────────────────────────────────────────────────────────┐
	│Things Today - 2015-09-26 16:02:52                                         │
	│┌─────────────────────────────────────────────────────────────────────────┐│
	││ Weather - Union City, NJ                                                ││
	││                                                                         ││
	││ Sat             Sun             Mon             Tue             Wed     ││
	││ 71F             74F             78F             78F             72F     ││
	││ 58F             65F             69F             68F             55F     ││
	││ Partly Cloudy   Partly Cloudy   PM Showers      Scattered Thund Sun     ││
	│└─────────────────────────────────────────────────────────────────────────┘│
	│┌────────────┐                                                             │
	││ Bus to NYC │                                                             │
	││            │                                                             │
	││ 16:05:24   │                                                             │
	││ 16:35:24   │                                                             │
	││ 17:05:24   │                                                             │
	││ 17:35:24   │                                                             │
	││ 18:05:24   │                                                             │
	│└────────────┘                                                             │
	└───────────────────────────────────────────────────────────────────────────┘

## Running

	$ python3 citty.py

## License

To the extent possible under law, the author(s) have dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. This software is distributed without any warranty.

You should have received a copy of the CC0 Public Domain Dedication along
with this software. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.

